#coding=utf8

import requests
import re
import lxml
from bs4 import BeautifulSoup
import ap
from pprint import pprint

#Configuration
session = requests.session()
username = ""
password = ""
page_Num = 1
show_Full = True
url = "http://140.127.113.136/StuPartTime/Announce/stu_announce_view.aspx?VCHASID="

if not ap.login(session, username, password):
	print "登入失敗"


#用lxml 解析
def viewPage_lxml(page_Num, show_Full, username):
	response = session.get(url+username)
	tree = lxml.etree.HTML(response.content)

	if page_Num != 1:
		X = tree.xpath(u"//input[@name='__VIEWSTATE']")[0].values()[3]
		Y = tree.xpath(u"//input[@name='__EVENTVALIDATION']")[0].values()[3]
		form = {
			"__EVENTTARGET":"GridView1",
			"__EVENTARGUMENT":"Page$%s"%page_Num,
			"__VIEWSTATE":X,
			"__EVENTVALIDATION":Y
		}
		response = session.post(url, data=form)
		tree = lxml.etree.HTML(response.content)

	id_list = []

	#tree.xpath(u"//table[@id='GridView1']//tr//td//span[contains(concat(' ', @id, ' '), 'Label1')]")
	
	n = tree.xpath(u"//table[@id='GridView1']//tr//td//td[5]")[0]
	print n.values()
	return 0


	for x in xrange(1,14):
		for y in tree.xpath(u"//table[@id='GridView1']//tr//td[%s]"%x):
			print y.text
		print "=================="

	return 0
	#單號
	tree.xpath(u"//table[@id='GridView1']//tr//td[1]")
	#發布日期
	tree.xpath(u"//table[@id='GridView1']//tr//td[2]")
	#需求人數
	tree.xpath(u"//table[@id='GridView1']//tr//td[3]")
	#工作時間
	tree.xpath(u"//table[@id='GridView1']//tr//td[4]")
	#條件
	tree.xpath(u"//table[@id='GridView1']//tr//td[5]")
	#聯絡人
	tree.xpath(u"//table[@id='GridView1']//tr//td[6]")
	#聯絡人分機
	tree.xpath(u"//table[@id='GridView1']//tr//td[7]")
	#發布單位
	tree.xpath(u"//table[@id='GridView1']//tr//td[8]")
	#已經截止
	tree.xpath(u"//table[@id='GridView1']//tr//td[9]")	
	#已經額滿
	tree.xpath(u"//table[@id='GridView1']//tr//td[10]")	
	#錄取
	tree.xpath(u"//table[@id='GridView1']//tr//td[11]")
	#應徵
	tree.xpath(u"//table[@id='GridView1']//tr//td[12]")
	#已應徵人數
	tree.xpath(u"//table[@id='GridView1']//tr//td[13]")

	table = tree.xpath(u"//table[@id='GridView1']")


	for x in table[0]:
		print x.text
		return 0
		if not show_Full:
			if x.text != "Y":
				id_list.append(x['id'])
		else:
			id_list.append(x['id'])

	
	for x in id_list:
		index = str(x).replace("lblFull", "")
		
		data = []
		#單號
		#data.append(bs.find('span', id=index+"Label1").text)
		#刊登日
		#data.append(bs.find('span', id=index+"Label2").text)
		#人數 取得刊登日parent.next
		print bs.find('span', id=index+"Label2").next_sibling
		#工作時間
		#data.append(bs.find('span', id=index+"Label3").text)
		#條件
		#data.append(bs.find('span', id=index+"Label4").text)
		#需求單位 取得條件parent.next
		for x in data:
			print x.encode("utf8")

		print "=========================="

	#print tree.xpath(u"//span[@id=re.compile(r'Label2$')]")
	

	#".//div[starts-with(@id,'comment-')"

#用BeautifulSoup 解析
def viewPage(page_Num, show_Full, username):
	response = session.get(url+username)
	bs = BeautifulSoup(response.content)
	if page_Num != 1:
		X = bs.find('input', type='hidden', name='__VIEWSTATE')['value']
		Y = bs.find('input', type='hidden', name='__EVENTVALIDATION')['value']
		form = {
			"__EVENTTARGET":"GridView1",
			"__EVENTARGUMENT":"Page$%s"%page_Num,
			"__VIEWSTATE":X,
			"__EVENTVALIDATION":Y
		}
		response = session.post(url, data=form)
		bs = BeautifulSoup(response.content)
	
	id_list = []
	table = bs.find('table', id='GridView1')
	for x in table.findAll('span', id=re.compile(r"lblFull$")):
		
		if not show_Full:
			if x.text != "Y":
				id_list.append(x['id'])
		else:
			id_list.append(x['id'])

	
	for x in id_list:
		index = str(x).replace("lblFull", "")
		
		data = []
		#單號
		#data.append(bs.find('span', id=index+"Label1").text)
		#刊登日
		#data.append(bs.find('span', id=index+"Label2").text)
		#人數 取得刊登日parent.next
		print bs.find('span', id=index+"Label2").next_sibling
		#工作時間
		#data.append(bs.find('span', id=index+"Label3").text)
		#條件
		#data.append(bs.find('span', id=index+"Label4").text)
		#需求單位 取得條件parent.next
		for x in data:
			print x.encode("utf8")

		print "=========================="



viewPage_lxml(1, show_Full, username)