# -*- coding: utf-8 -*-

import os
import json
import redis
import hashlib
import requests
from werkzeug.contrib.cache import SimpleCache


import kuas_api.kuas.ap as ap
import kuas_api.kuas.leave as leave
import kuas_api.kuas.parse as parse
import kuas_api.kuas.bus as bus
import kuas_api.kuas.notification as notification
import kuas_api.kuas.news as news
from lxml import etree

AP_QUERY_EXPIRE = 3600
BUS_EXPIRE_TIME = 0
SERVER_STATUS_EXPIRE_TIME = 180
NOTIFICATION_EXPIRE_TIME = 3600

BUS_QUERY_TAG = "bus"
NOTIFICATION_TAG = "notification"

#: AP guest account
AP_GUEST_ACCOUNT = "guest"

#: AP guest password
AP_GUEST_PASSWORD = "123"

s_cache = SimpleCache()
red = redis.StrictRedis.from_url(url= os.environ['REDIS_URL'],db=2)
SECRET_KEY = red.get("SECRET_KEY") if red.exists(
    "SECRET_KEY") else str(os.urandom(32))


def dump_session_cookies(session,is_login):
    """Dumps cookies to list
    """

    cookies = []
    for c in session.cookies:
        cookies.append({
            'name': c.name,
            'domain': c.domain,
            'value': c.value})

    return {'is_login': is_login, 'cookies':cookies}


def login(username, password):
    session = requests.Session()
    is_login = {}

    # AP Login
    try:
        is_login["ap"] = ap.login(session, username, password)
    except:
        is_login["ap"] = False

    # Login bus system
    try:
        bus.init(session)
        is_login["bus"] = bus.login(session, username, password)
    except:
        is_login["bus"] = False

    # Login leave system
    try:
        is_login["leave"] = leave.login(session, username, password)
    except:
        is_login["leave"] = False
    if is_login["ap"]: 
        return dump_session_cookies(session,is_login)
    else:
        return False 


def ap_query(session, qid=None, args=None,
             username=None, expire=AP_QUERY_EXPIRE):
    ap_query_key_tag = str(username) + str(args) +  str(SECRET_KEY)
    ap_query_key = qid + \
        hashlib.sha512(
            bytes(ap_query_key_tag, "utf-8")).hexdigest()

    if not red.exists(ap_query_key):
        ap_query_content = parse.parse(qid, ap.query(session, qid, args))

        red.set(ap_query_key, json.dumps(ap_query_content, ensure_ascii=False))
        red.expire(ap_query_key, expire)
    else:
        ap_query_content = json.loads(red.get(ap_query_key))

    return ap_query_content

def leave_query(session, year="102", semester="2"):
    return leave.getList(session, year, semester)


def leave_submit(session, start_date, end_date,
                 reason_id, reason_text, section):
    leave_dict = {"reason_id": reason_id,
                  "reason_text": reason_text, "section": section}

    return leave.submitLeave(session, start_date, end_date, leave_dict)


def bus_query(session, date):
    bus_cache_key = BUS_QUERY_TAG + date.replace("-", "")

    if not red.exists(bus_cache_key):
        bus_q = bus.query(session, *date.split("-"))

        red.set(bus_cache_key, json.dumps(bus_q, ensure_ascii=False))
        red.expire(bus_cache_key, BUS_EXPIRE_TIME)
    else:
        bus_q = json.loads(red.get(bus_cache_key))

    # Check if have reserve, and change isReserve value to 0
    reserve = bus_reserve_query(session)

    for q in bus_q:
        q['isReserve'] = 0
        q['cancelKey'] = 0

        for r in reserve:
            if (r['time'] == q['runDateTime'] and
                    r['end'] == q['endStation']):
                q['isReserve'] = 1
                q['cancelKey'] = r['cancelKey']
                break

    return bus_q


def bus_reserve_query(session):
    return bus.reserve(session)


def bus_booking(session, busId, action):
    return bus.book(session, busId, action)


def notification_query(page=1):
    notification_page = NOTIFICATION_TAG + str(page)
    red_query = red.get(notification_page)
    red_query = False if red_query is None or red_query == '[]' else True

    if not red_query:
        notification_content = notification.get(page)

        red.set(notification_page,
                json.dumps(notification_content, ensure_ascii=False))
        red.expire(notification_page, NOTIFICATION_EXPIRE_TIME)
    else:
        notification_content = json.loads(red.get(notification_page))

    return notification_content


def news_query():
    return news.news()


def news_status():
    return news.news_status()


def server_status():
    if not s_cache.get("server_status"):
        ap_status = ap.status()
        leave_status = leave.status()
        bus_status = bus.status()

        server_status = [ap_status, leave_status, bus_status]

        s_cache.set(
            "server_status", server_status, timeout=SERVER_STATUS_EXPIRE_TIME)
    else:
        server_status = s_cache.get("server_status")

    return server_status


def get_semester_list():
    """Get semester list from ap system.

    :rtype: dict

    >>> get_semester_list()[-1]['value']
    '92,2'
    """

    s = requests.Session()
    ap.login(s,AP_GUEST_ACCOUNT, AP_GUEST_PASSWORD)

    content = ap_query(s, "ag304_01")
    if len(content)<3000:
        return False
    root = etree.HTML(content)

    #options = root.xpath("id('yms_yms')/option")
    try:
        options = map(lambda x: {"value": x.values()[0].replace("#", ","),
                                "selected": 1 if "selected" in x.values() else 0,
                                "text": x.text},
                    root.xpath("id('yms_yms')/option")
                    )
    except:
        return False
    
    options = list(options)

    return options



if __name__ == "__main__":
    s = requests.Session()
    is_login = login(s, "guest", "123")

    print(is_login)