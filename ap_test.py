# -*- coding: utf-8 -*-

import requests

USERNAME = "guest"
PASSWORD = "123"

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

    print("[*] Pass test :)")

if __name__ == "__main__":
    process()
