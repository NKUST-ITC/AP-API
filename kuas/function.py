#-*- coding: utf-8 -*-

import time
import requests
from lxml import etree
from werkzeug.contrib.cache import SimpleCache

import ap
import leave
import bus
import notification

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
        bus.login(session, username, password)
        is_login = True
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
    return leave.submitLeave(session, start_date, end_date, reason_id, reason_text, section)


def bus_query(session, date):
    return bus.query(session, *date.split("-"))


def bus_booking(session, busId, action):
    return bus.book(session, busId, action)
    

def notification_query(page=1):
    return notification.get(page)
    

def server_status():
    if not cache.get("server_status"):
        ap_status = ap.status()
        leave_status = leave.status()
        bus_status = bus.status()

        server_status = [ap_status, leave_status, bus_status]

        cache.set("server_status", server_status, timeout=180)
    else:
        server_status = cache.get("server_status")


    return server_status
    

if __name__ == "__main__":
    import requests
    s = requests.Session()
    is_login = login(s, "guest", "123")

    print(is_login)
