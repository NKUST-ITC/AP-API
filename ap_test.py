# -*- coding: utf-8 -*-

import requests

USERNAME = "1102108133"
PASSWORD = ""

URL = "http://kuas.grd.idv.tw:14768/"


def process():
    s = requests.Session()

    try:
        r = s.get(URL)
        print("[*] Server found, ready to test!")
    except Exception as e:
        print("[-] Server Error!!! Must to reset!!!")
        print(e)
        return

    try:
        r = s.post(URL + "ap/login", data={"username": USERNAME, "password": PASSWORD})
        if r.text.startswith("true"):
            print("[*] Login Success")
        else:
            print("[-] Login fail, incorrect username or password")
            return
    except Exception as e:
        print("[-] Server Error!!! Fail to login")
        print(e)
        return

    try:
        r = s.post(URL + "ap/query", data={"arg01": "103", "arg02": "01", "arg03": "1102108133", "fncid": "ag008"})
        if not r.text.startswith("false"):
            print("[*] AP Query success")
        else:
            print("[-] AP Query fail")
            return
    except Exception as e:
        print("[-] AP Query fatal error")
        print(e)
        return

    
    try:
        r = s.post(URL + "bus/query", data={"date": "2014-10-30"})
        print("[*] Bus Query success")
        print("    - %s" % r.text[:100])
    except Exception as e:
        print("[-] Bus Query fatal error")
        print(e)
        return 

    try:
        r = s.post(URL + "leave", data={"arg01": "102", "arg02": "01"})
        if not r.text.startswith("false"):
            print("[*] Leave Query success")
            print("    - %s" % r.text)
        else:
            print("[-] Leave Query fail")
            return
    except Exception as e:
        print("[-] Leave Query fatal error")
        print(e)
        return

    

    print("[*] Pass test :)")

if __name__ == "__main__":
    process()
