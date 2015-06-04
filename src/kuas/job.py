#coding=utf8

import requests
import re
import time
import lxml
import json
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

	#不是第一頁的話，需要抓取google 分析的input
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

		#tree.xpath(u"//table[@id='GridView1']//tr//td//span[contains(concat(' ', @id, ' '), 'Label1')]")
	



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


#以下開始
# viewPage_lxml(1, show_Full, username)
response = session.get(url+username)
tree = lxml.etree.HTML(response.content)
result = []


#抓取公告編號
ID = []
for x in tree.xpath(u"//table[@id='GridView1']//tr//td//span[contains(concat(' ', @id, ' '), 'Label1')]"):
	ID.append(x.text)

#抓取刊登時間以及需求人數
post_date = []
person = []
for x in tree.xpath(u"//table[@id='GridView1']//tr//td//span[contains(concat(' ', @id, ' '), 'Label2')]"):
	post_date.append(x.text)
	person.append(x.getparent().getparent().getnext().getchildren()[0].text)

#抓取時間
work_time = []
for x in tree.xpath(u"//table[@id='GridView1']//tr//td//span[contains(concat(' ', @id, ' '), 'Label3')]"):
	work_time.append(x.text)

#抓取需求、聯絡人、電話、需求單位
work_required = []
contact_name = []
contact_number = []
contact_org = []
for x in tree.xpath(u"//table[@id='GridView1']//tr//td//span[contains(concat(' ', @id, ' '), 'Label4')]"):
	#這個是工作需求，但是中文還沒搞定
	work_required.append(x.text)
	
	#因為聯絡人、電話、需求單位沒有特徵可以直接取得，所以使用以下方法
	contact_name_tag = x.getparent().getparent().getnext()
	#聯絡人姓名，但是中文還沒搞定
	contact_name.append(contact_name_tag.getchildren()[0].text)
	
	#取得電話
	contact_number_tag = contact_name_tag.getnext()
	contact_number.append(contact_number_tag.getchildren()[0].text)

	#取得需求單位，但是中文還沒搞定
	contact_org_tag = contact_number_tag.getnext()
	contact_org.append(contact_org_tag.getchildren()[0].text)


total = [ID, post_date, person, work_time, work_required, contact_name, contact_number, contact_org]


for i, v in enumerate(total):
	total[i] = eval(str(v).replace("u\'", "\'"))

total = json.dumps(total)
