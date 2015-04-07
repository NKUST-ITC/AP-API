#-*- encoding=utf-8 -*-

import requests
from lxml import etree

AP_BASE_URL = "http://140.127.113.227"
AP_LOGIN_URL = AP_BASE_URL + "/kuas/perchk.jsp"
AP_FNC_URL = AP_BASE_URL + "/kuas/fnc.jsp"
AP_QUERY_URL = AP_BASE_URL + "/kuas/%s_pro/%s.jsp?"

RANDOM_ID = "AG009"

LOGIN_TIMEOUT = 1.0
QUERY_TIMEOUT = 5.0
RANDOM_TIMEOUT = 1.0


def status():
    ap_status = False

    try:
        ap_status = login(requests, "guest", "123")
    except:
        pass

    return ap_status


def login(session, username, password):
    payload = {"uid": username, "pwd": password}

    r = session.post(AP_LOGIN_URL, data=payload, timeout=LOGIN_TIMEOUT)

    root = etree.HTML(r.text)

    try:
        is_login = not root.xpath("//script")[-1].text.startswith("alert")
    except:
        is_login = False


    return is_login


def query(session, qid=None, args=None):
    #ls_random = random_number(session, RANDOM_ID)
    data = {"arg01": "", "arg02": "", "arg03": "",
                "fncid": "", "uid": "", "ls_randnum": ""}

    #data['ls_randnum'] = ls_random
    data['fncid'] = qid

    for key in args:
        data[key] = args[key]

    try:
        content = session.post(AP_QUERY_URL % (qid[:2], qid), data=data, timeout=QUERY_TIMEOUT).content
    except requests.exceptions.ReadTimeout:
        content = ""

    return content


def random_number(session, fncid):
    raw_data = {"fncid": fncid, "sysyear": "103", "syssms":
                "1", "online": "okey", "loginid": "1102108130"}
    r = session.post(AP_FNC_URL, data=raw_data, timeout=RANDOM_TIMEOUT)

    root = etree.HTML(r.text)
    lsr = root.xpath("//input")[-1].values()[-1]

    return lsr



if __name__ == "__main__":
    s = requests.Session()
    is_login = login(s, "guest", "123")
    
    print(is_login)
