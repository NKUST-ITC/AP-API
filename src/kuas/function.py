#-*- coding: utf-8 -*-

import os
import time
import json
import redis
import datetime
import hashlib
import requests
from lxml import etree
from werkzeug.contrib.cache import SimpleCache


import ap
import leave
import parse
import bus
import notification
import news


AP_QUERY_EXPIRE = 0
BUS_EXPIRE_TIME = 1800
SERVER_STATUS_EXPIRE_TIME = 180
NOTIFICATION_EXPIRE_TIME = 1800

BUS_QUERY_TAG = "bus"
NOTIFICATION_TAG = "notification"

cache = SimpleCache()
red = redis.StrictRedis(db=0)
SERECT_KEY = str(os.urandom(32))


def login(session, username, password):
    is_login = {}

    # AP Login
    try:
        is_login["ap"] = ap.login(session, username, password)
    except:
        pass


    # Login bus system
    try:
        bus.init(session)
        is_login["bus"] = bus.login(session, username, password)
    except:
        pass


    # Login leave system
    try:
        is_login["leave"] = leave.login(session, username, password)
    except:
        pass


    return all(is_login.values())


def ap_query(session, qid=None, args=None, username=None, expire=AP_QUERY_EXPIRE):
    ap_query_key = qid + hashlib.sha512(str(username) + str(args) + SERECT_KEY).hexdigest()

    if not red.exists(ap_query_key):
        ap_query_content = parse.parse(qid, ap.query(session, qid, args))

        red.set(ap_query_key, json.dumps(ap_query_content))
        red.expire(ap_query_key, expire)
    else:
        ap_query_content = json.loads(red.get(ap_query_key))


    return ap_query_content


def leave_query(session, year="102", semester="2"):
    return leave.getList(session, year, semester)


def leave_submit(session, start_date, end_date, reason_id, reason_text, section):
    leave_dict = {"reason_id": reason_id, "reason_text": reason_text, "section": section}

    return leave.submitLeave(session, start_date, end_date, leave_dict)


def bus_query(session, date):
    bus_cache_key = BUS_QUERY_TAG + date.replace("-", "")

    #if not cache.get(bus_cache_key):
    if not red.exists(bus_cache_key):
        bus_q = bus.query(session, *date.split("-"))
        for q in bus_q:
            q['isReserve'] = -1

        #cache.set(bus_cache_key, bus_q, timeout=BUS_EXPIRE_TIME)
        red.set(bus_cache_key, json.dumps(bus_q))
        red.expire(bus_cache_key, BUS_EXPIRE_TIME)
    else:
        #bus_q = cache.get(bus_cache_key)
        bus_q = json.loads(red.get(bus_cache_key))

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
    notification_page = NOTIFICATION_TAG + str(page)
    red_query = red.get(notification_page)
    red_query = False if red_query == None or red_query == '[]' else True

    if not red_query:
        notification_content = notification.get(page)

        red.set(notification_page, json.dumps(notification_content))
        red.expire(notification_page, NOTIFICATION_EXPIRE_TIME)
    else:
        notification_content = json.loads(red.get(notification_page))


    return notification_content

    

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

        cache.set("server_status", server_status, timeout=SERVER_STATUS_EXPIRE_TIME)
    else:
        server_status = cache.get("server_status")


    return server_status
    

if __name__ == "__main__":
    import requests
    s = requests.Session()
    is_login = login(s, "guest", "123")

    print(is_login)
