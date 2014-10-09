#-*- coding: utf-8 -*-

import time
import json
import requests
from lxml import etree
from werkzeug.contrib.cache import SimpleCache

import ap
import leave
import bus
import notification
import news


BUS_TIMEOUT = 1800
SERVER_STATUS_TIMEOUT = 180
BUS_QUERY_TAG = "bus_query"

cache = SimpleCache()

def login(session, username, password):
    is_login = False

    # AP Login
    try:
        is_login = ap.login(session, username, password)
    except:
        pass


    # Login bus system
    try:
        bus.init(session)
        is_login = bus.login(session, username, password)
    except:
        pass


    # Login leave system
    try:
        is_login = leave.login(session, username, password)
    except:
        pass


    return is_login


def ap_query(session, qid=None, args=None):
    return ap.query(session, qid, args)


def leave_query(session, year="102", semester="2"):
    return leave.getList(session, year, semester)


def leave_submit(session, start_date, end_date, reason_id, reason_text, section):
    leave_dict = {"reason_id": reason_id, "reason_text": reason_text, "section": section}

    return leave.submitLeave(session, start_date, end_date, leave_dict)


def bus_query(session, date):
    bus_cache_key = BUS_QUERY_TAG + date

    if not cache.get(bus_cache_key):
        bus_q = bus.query(session, *date.split("-"))
        for q in bus_q:
            q['isReserve'] = -1

        cache.set(bus_cache_key, bus_q, timeout=BUS_TIMEOUT)
    else:
        bus_q = cache.get(bus_cache_key)

    # Check if have reserve, and change isReserve value to 0
    reserve = bus_reserve_query(session)

    for r in reserve:
        for q in bus_q:
            if r['time'] == q['runDateTime']:
                q['isReserve'] = 0
                break
    

    return bus_q


def bus_reserve_query(session):
    return bus.reserve(session)


def bus_booking(session, busId, action):
    return bus.book(session, busId, action)
    

def notification_query(page=1):
    return notification.get(page)
    

def news_query():
    return news.news()


def news_status():
    return news.news_status()


def server_status():
    if not cache.get("server_status"):
        ap_status = ap.status()
        leave_status = leave.status()
        bus_status = bus.status()

        server_status = [ap_status, leave_status, bus_status]

        cache.set("server_status", server_status, timeout=SERVER_STATUS_TIMEOUT)
    else:
        server_status = cache.get("server_status")


    return server_status
    

if __name__ == "__main__":
    import requests
    s = requests.Session()
    is_login = login(s, "guest", "123")

    print(is_login)
