#-*- coding: utf-8 -*-

import time
import hashlib
import requests
from lxml import etree

import leave
import bus

RANDOM_ID = "AG009"

ap_login_url = "http://140.127.113.227/kuas/perchk.jsp"
fnc_url = "http://140.127.113.227/kuas/fnc.jsp"

query_url = "http://140.127.113.227/kuas/%s_pro/%s.jsp?"

sd = {}


def hash(f):
	result = hashlib.sha256(f + str(time.time())).hexdigest()
	for i in range(48):
		result = hashlib.sha256(result).hexdigest()

	return result


def login(username, password):
    s = requests.Session()

    # AP Login
    payload = {"uid": username, "pwd": password}

    r = s.post(ap_login_url, data=payload)


    root = etree.HTML(r.text)
    is_login = not root.xpath("//script")[-1].text.startswith("alert")

    if is_login:
        hash_value = hash(username)

        # Login leave system
        leave.login(s, username, password)

        # Login bus system
        bus.init(s)
        bus.login(s, username, password)

        sd[hash_value] = s

        return hash_value
    else:
        return None

def is_login(hash_value):
    if hash_value in sd:
        return True
    else:
        return False



def query(hash_value, username=None, password=None, qid=None, args=None):
    ls_random = random_number(hash_value, RANDOM_ID)
    payload = {"arg01": "", "arg02": "", "arg03": "",
                "fncid": "", "uid": "", "ls_randnum": ""}

    payload['ls_randnum'] = ls_random
    payload['fucid'] = qid
    payload["arg01"] = args["arg01"]
    payload["arg02"] = args["arg02"]
    payload["arg03"] = username
    r = sd[hash_value].post(query_url % (qid[:2], qid), data=payload)

    return r.content


def leave_query(hash_value, year="102", semester="2"):
    return leave.getList(sd[hash_value], year, semester)


def bus_query(hash_value, date):
    return bus.query(sd[hash_value], *date.split("-"))


def random_number(hash_value, fncid):
    raw_data = {"fncid": fncid, "sysyear": "103", "syssms":
                "1", "online": "okey", "loginid": "1102108130"}
    r = sd[hash_value].post(fnc_url, data=raw_data)

    root = etree.HTML(r.text)
    lsr = root.xpath("//input")[-1].values()[-1]

    return lsr


if __name__ == "__main__":
    pass