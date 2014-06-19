#-*- coding: utf-8 -*-

import requests


RANDOM_ID = "AG009"

login_url = "http://140.127.113.227/kuas/perchk.jsp"
fnc_url = "http://140.127.113.227/kuas/fnc.jsp"

query_url = "http://140.127.113.227/kuas/%s_pro/%s.jsp?"

s = requests.Session()
def login( uid , pwd ):
    response = s.post( "http://ap.kuas.edu.tw/kuas/perchk.jsp", data={"uid":uid,"pwd":pwd}).text

    if response.find('f_index.html') != -1 :
        print(str(uid) + "," + pwd)
        with open("s.log", 'a') as l:
            l.write( str(uid) + "," + pwd + "\n")
        return True
    else :
        return False



def query(qid, username, password, *args):
    login(username, password)
    ls_random = random_number(RANDOM_ID)

    payload = {"arg01": "", "arg02": "", "arg03": "",
                "fncid": "", "uid": "", "ls_randnum": ""}

    payload['ls_randnum'] = ls_random
    payload['fucid'] = qid

    r = s.post(query_url % (qid[:2], qid), data=payload)

    return r.content



def random_number(fncid):
    raw_data = {"fncid": fncid, "sysyear": "103", "syssms":
                "1", "online": "okey", "loginid": "1102108131"}
    response = session.post(fnc_url, data=raw_data)
    root = BeautifulSoup(response.text)
    ans = root.findAll("input", {"type": "hidden", "name": "ls_randnum"})
    ls_randnum = ans[0]['value']
    return ls_randnum


if __name__ == "__main__":
	login("1102108133", "111")