#-*- encoding=utf-8 -*-

from lxml import etree
import requests


ap_login_url = "http://140.127.113.231/kuas/perchk.jsp"
fnc_url = "http://140.127.113.231/kuas/fnc.jsp"
query_url = "http://140.127.113.231/kuas/%s_pro/%s.jsp?"

RANDOM_ID = "AG009"
LOGIN_TIMEOUT = 1.0
QUERY_TIMEOUT = 1.0
RANDOM_TIMEOUT = 1.0



def login(session, username, password):
    payload = {"uid": username, "pwd": password}

    r = session.post(ap_login_url, data=payload, timeout=LOGIN_TIMEOUT)

    root = etree.HTML(r.text)

    try:
        is_login = not root.xpath("//script")[-1].text.startswith("alert")
    except:
        is_login = False


    return is_login


def query(session, qid=None, args=None):
    ls_random = random_number(session, RANDOM_ID)
    payload = {"arg01": "", "arg02": "", "arg03": "",
                "fncid": "", "uid": "", "ls_randnum": ""}

    payload['ls_randnum'] = ls_random
    payload['fucid'] = qid
    
    for key in args:
        payload[key] = args[key]

    r = session.post(query_url % (qid[:2], qid), data=payload, timeout=QUERY_TIMEOUT)

    return r.content


def random_number(session, fncid):
    raw_data = {"fncid": fncid, "sysyear": "103", "syssms":
                "1", "online": "okey", "loginid": "1102108130"}
    r = session.post(fnc_url, data=raw_data, timeout=RANDOM_TIMEOUT)

    root = etree.HTML(r.text)
    lsr = root.xpath("//input")[-1].values()[-1]

    return lsr


if __name__ == "__main__":
    s = requests.Session()
    is_login = login(s, "guest", "123")
    

    print(is_login)
