#-*- coding: utf-8 -*-

import time
import requests
from lxml import etree

import ap
import leave
import bus
import notification


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
        leave.login(session, username, password)
        is_login = True
    except:
        pass

    
    return is_login


def ap_query(session, qid=None, args=None):
    return ap.query(session, qid, args)


def leave_query(session, year="102", semester="2"):
    return leave.getList(session, year, semester)


def bus_query(session, date):
    return bus.query(session, *date.split("-"))


def bus_booking(session, busId, action):
    return bus.book(session, busId, action)
    

def notification_query(page=1):
    return notification.get(page)
    

def server_status():
    ap_status = False 
    leave_status = 400
    bus_status = 400


    try:
        ap_status = ap.login(requests, "guest", "123")
    except:
        pass

    try:
        leave_status = requests.head("http://leave.kuas.edu.tw").status_code
    except:
        pass

    try:
        bus_status = requests.head("http://bus.kuas.edu.tw", proxies={"http": "http://127.0.0.1:8000"}).status_code
    except:
        pass


    return [ap_status, leave_status, bus_status]


if __name__ == "__main__":
    import requests
    s = requests.Session()
    is_login = login(s, "guest", "123")

    print(is_login)
