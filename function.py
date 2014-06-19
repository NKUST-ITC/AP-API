#-*- coding: utf-8 -*-
import threading
import requests
import json
import os
import sys
import uniout
import collections
from lxml import etree
from bs4 import BeautifulSoup

session = requests.session()
logurl = "http://140.127.113.227/kuas/perchk.jsp"
fnc_url="http://140.127.113.227/kuas/fnc.jsp"
score_url="http://140.127.113.227/kuas/ag_pro/ag222.jsp?"

def login(account, password):
	payload = {"uid": account,"pwd": password}
	response = session.post(logurl, data = payload)

	if "密碼不正確" in response.content :
		return "False"
	else :
		return "True"
	
def curriculum(AGID,account, password):
	login(account,password)
	ls_randnum=randnum("AG009")
	raw_data={"arg01":"103","arg02":"1","arg03":account,"fncid":AGID,"uid":account,"ls_randnum":ls_randnum}
	response = session.post(score_url, data = raw_data)
	return response.content
def randnum(fncid):
	raw_data={"fncid":fncid,"sysyear":"103","syssms":"1","online":"okey","loginid":"1102108131"}
	response = session.post(fnc_url, data = raw_data)
	root = BeautifulSoup(response.text)
	ans=root.findAll("input", {"type": "hidden", "name": "ls_randnum"})
	ls_randnum=ans[0]['value']
	return ls_randnum