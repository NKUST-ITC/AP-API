#-*- encoding=utf-8

import time
import requests
from lxml import etree

s = requests.session()

SUBMIT_LEAVE_URL = "http://leave.kuas.edu.tw/CK001MainM.aspx"

def login(session, username, password):
    root = etree.HTML(session.get("http://leave.kuas.edu.tw").text)


    form = {}
    for i in root.xpath("//input"):
        form[i.attrib['name']] = ""
        if "value" in i.attrib:
            form[i.attrib['name']] = i.attrib['value']


    form['Login1$UserName'] = username
    form['Login1$Password'] = password

    session.post('http://leave.kuas.edu.tw/', data=form)


def getList(session, year="102", semester="2"):
    root = etree.HTML(session.get("http://leave.kuas.edu.tw/AK002MainM.aspx").text)
    
    form = {}
    for i in root.xpath("//input"):
        form[i.attrib["name"]] = i.attrib["value"]

    form['ctl00$ContentPlaceHolder1$SYS001$DropDownListYms'] = "%s-%s" % (year, semester)
    
    root = etree.HTML(session.post("http://leave.kuas.edu.tw/AK002MainM.aspx", data=form).text)
    
    tr = root.xpath("//table")[-1]

    result = []

    # Delete row id, leave id, teacher quote
    token_night = False
    for r_index, r in enumerate(tr):
        r = list(map(lambda x: x.replace("\r", "").
                                replace("\n", "").
                                replace("\t", "").
                                replace(u"\u3000", "").
                                replace(" ", ""),
                        r.itertext()
                        ))

        if not r[0]: del r[0]
        if not r[-1]: del r[-1]

        r = r[2:]

        # Detect if night class have dismiss class
        for c in r[-5:]:
            if c and r_index:
                token_night = True

        # Teacher quote
        try:
            del r[1]
        except:
            pass


        result.append(r)

    if not token_night:
        for index, r in enumerate(result):
            result[index] = result[index][:-5]

    if result == [[]]:
        result = [["本學期無缺曠課記錄"]]

    return result

def submitLeave(session, start_date, end_date, leave_dict):
    """Submit leave data to leave.kaus.edu.tw
    session: The session include login cookies
    start_date: Start date for leave
    end_date: End date for leave
    leave_dict: A dict with data include which section were leave
        reason_id: String, 21 ~ 26.
        reason_text: String, a reason why leave.
        section: List, the number which count on it.

    """


    # First page
    r = session.get(SUBMIT_LEAVE_URL)

    root = etree.HTML(r.text)

    d = {i.attrib['name']:i.attrib['value'] for i in root.xpath("//input")}
    del d['ctl00$ButtonLogOut']

    # Setting start date and end date
    r = session.post(SUBMIT_LEAVE_URL, data=d)
    root = etree.HTML(r.text)

    d = {i.attrib['name']:i.attrib['value']  for i in root.xpath("//input[starts-with(@id, '__')]")}
    d["ctl00$ContentPlaceHolder1$CK001$DateUCCBegin$text1"] = start_date
    d["ctl00$ContentPlaceHolder1$CK001$DateUCCEnd$text1"] = end_date
    d["ctl00$ContentPlaceHolder1$CK001$ButtonCommit"] = u"下一步"

    # Setting leaving section
    r = session.post(SUBMIT_LEAVE_URL, data=d)
    root = etree.HTML(r.text)

    reason_map = {"21": u"事", "22": u"病", "23": u"公", "24": u"喪", "26": u"產"}
    
    # Setting reason id
    d = {i.attrib['name']:i.attrib['value']  for i in root.xpath("//input[starts-with(@id, '__')]")}
    d['ctl00$ContentPlaceHolder1$CK001$RadioButtonListOption'] = leave_dict["reason_id"]
    d['ctl00$ContentPlaceHolder1$CK001$TextBoxReason'] = ""
    r = session.post(SUBMIT_LEAVE_URL, data=d)


    # Setting leaving button
    button = root.xpath("//input[starts-with(@id, 'ContentPlaceHolder1_CK001_GridViewMain_Button_')]")

    for i in leave_dict["section"]:
        root = etree.HTML(r.text)
        d = {i.attrib['name']:i.attrib['value']  for i in root.xpath("//input[starts-with(@id, '__')]")}
        d['ctl00$ContentPlaceHolder1$CK001$RadioButtonListOption'] = leave_dict["reason_id"]
        d['ctl00$ContentPlaceHolder1$CK001$TextBoxReason'] = leave_dict['reason_text']
        d['ctl00$ContentPlaceHolder1$CK001$DropDownListTeacher'] = root.xpath("//option[@selected='selected']")[0].values()[-1]
        d[button[int(i)].attrib['name']] = ''
        d['__ASYNCPOST'] = "ture"
        r = session.post(SUBMIT_LEAVE_URL, data=d)


    # Send to last step
    root = etree.HTML(r.text)
    d = {i.attrib['name']:i.attrib['value']  for i in root.xpath("//input[starts-with(@id, '__')]")}
    d['ctl00$ContentPlaceHolder1$CK001$TextBoxReason'] = leave_dict['reason_text']
    d['ctl00$ContentPlaceHolder1$CK001$ButtonCommit2'] = u"下一步"
    r = session.post(SUBMIT_LEAVE_URL, data=d)

    # Save leaving submit
    root = etree.HTML(r.text)
    d = {i.attrib['name']:i.attrib['value']  for i in root.xpath("//input[starts-with(@id, '__')]")}
    d['ctl00$ContentPlaceHolder1$CK001$ButtonSend'] = '存檔'
    files = {"ctl00$ContentPlaceHolder1$CK001$FileUpload1": (" ", "", "application/octet-stream")}
    
    # Send to server and save the submit
    #r = session.post(SUBMIT_LEAVE_URL, files=files, data=d)




if __name__ == '__main__':
    login(s, "1102108133", "111")
    submitLeave(s, '103/09/15', '103/09/15', {"reason_id": "21", "reason_text": "testing", "section": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]})
    #print(getList(s, "103", "1"))

