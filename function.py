#-*- coding: utf-8 -*-

import time
import hashlib
from lxml import etree

import ap
import leave
import bus
import notification


def login(session, username, password):
    # AP Login
    is_login = ap.login(session, username, password)

    if is_login:
        # Login bus system
        bus.init(session)
        bus.login(session, username, password)

        # Login leave system
        leave.login(session, username, password)

        return True
    else:
        return None


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
    


if __name__ == "__main__":
    import requests
    s = requests.Session()
    is_login = login(s, "guest", "123")

    print(is_login)