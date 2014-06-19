# -*- coding: utf-8 -*-

import collections
import uniout
import requests

login_URL = "http://127.0.0.1:5000/ap/login"
curriculum_URL="http://127.0.0.1:5000/ap/curriculum"
session = requests.session()


def Login(account,password):

	#raw_data = {"AGID":"AG222","account":account,"password":password}
	raw_data = {"account":account,"password":password}

	response = session.post(login_URL , data = raw_data)

	print response.content.encode('utf-8')
def Search(AGID,account,password):

	raw_data = {"AGID":AGID,"account":account,"password":password}
	#raw_data = {"account":account,"password":password}

	response = session.post(curriculum_URL , data = raw_data)
	print response.content.decode('utf-8').encode('utf-8')
