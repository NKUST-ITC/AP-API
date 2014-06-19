#-*- coding: utf-8 -*-

import requests
from lxml import etree


RANDOM_ID = "AG009"

login_url = "http://140.127.113.227/kuas/perchk.jsp"
fnc_url = "http://140.127.113.227/kuas/fnc.jsp"

query_url = "http://140.127.113.227/kuas/%s_pro/%s.jsp?"

s = requests.Session()

def login(username, password):
    #global s

    #s = requests.Session()

    payload = {"uid": username, "pwd": password}
    r = s.post(login_url, data=payload)


    root = etree.HTML(r.text)
    is_login = not root.xpath("//script")[-1].text.startswith("alert")


    return is_login



def query(username=None, password=None, qid=None, *args):
    #login(username, password)
    ls_random = random_number(RANDOM_ID)

    payload = {"arg01": "", "arg02": "", "arg03": "",
                "fncid": "", "uid": "", "ls_randnum": ""}

    payload['ls_randnum'] = ls_random
    payload['fucid'] = qid
    payload["arg01"] = "103"
    payload["arg02"] = "01"

    r = s.post(query_url % (qid[:2], qid), data=payload)

    return r.content



def random_number(fncid):
    raw_data = {"fncid": fncid, "sysyear": "103", "syssms":
                "1", "online": "okey", "loginid": "1102108130"}
    r = s.post(fnc_url, data=raw_data)

    root = etree.HTML(r.text)
    lsr = root.xpath("//input")[-1].values()[-1]

    return lsr


if __name__ == "__main__":
	pass