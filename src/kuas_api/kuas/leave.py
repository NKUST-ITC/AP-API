#-*- encoding=utf-8

import requests
from lxml import etree

s = requests.session()

SUBMIT_LEAVE_URL = "http://leave.nkust.edu.tw/CK001MainM.aspx"

TIMEOUT = 5.0


def status():
    leave_status = 400

    try:
        leave_status = requests.head(
            "http://leave.nkust.edu.tw/", timeout=TIMEOUT).status_code
    except:
        pass

    return leave_status


def login(session, username, password):
    try:
        session.headers.update({
        'Origin': 'http://leave.nkust.edu.tw',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://leave.nkust.edu.tw/LogOn.aspx',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6'
            })
        r = session.get("http://leave.nkust.edu.tw/LogOn.aspx", timeout=TIMEOUT)
    except requests.exceptions.ReadTimeout:
        return False
    root = etree.HTML(r.text)

    form = {}
    for i in root.xpath("//input"):
        form[i.attrib['name']] = ""
        if "value" in i.attrib:
            form[i.attrib['name']] = i.attrib['value']

    form['Login1$UserName'] = username
    form['Login1$Password'] = password
    form['__EVENTTARGET	'] = ''
    form['__EVENTARGUMENT	']=''


    r = session.post('http://leave.nkust.edu.tw/LogOn.aspx', data=form)

    root = etree.HTML(r.text)

    if root.xpath("//td[@align='center' and @style='color:Red;' and @colspan='2']"):
        return False
    else:
        return True


def getList(session, year="102", semester="2"):
    root = etree.HTML(
        session.get("http://leave.nkust.edu.tw/AK002MainM.aspx").text)

    form = {}
    for i in root.xpath("//input"):
        form[i.attrib["name"]] = i.attrib[
            "value"] if "value" in i.attrib else ""
    #print(form)
    del form['ctl00$ButtonLogOut']

    form[
        'ctl00$ContentPlaceHolder1$SYS001$DropDownListYms'] = "%s-%s" % (year, semester)

    r = session.post(
        "http://leave.nkust.edu.tw/AK002MainM.aspx", data=form)
    root = etree.HTML(r.text)

    tr = root.xpath("//table")[-1]

    leave_list = []

    # Delete row id, leave id, teacher quote
    for r_index, r in enumerate(tr):
        r = list(map(lambda x: x.replace("\r", "").
                     replace("\n", "").
                     replace("\t", "").
                     replace(u"\u3000", "").
                     replace(" ", ""),
                     r.itertext()
                     ))

        if not r[0]:
            del r[0]
        if not r[-1]:
            del r[-1]

        leave_list.append(r)
    result = []
    for r in leave_list[1:]:
        i = len(r)-15
        for approved in range(4,i):
            r[3]+= ' , '+r[approved]
        leave = {
            "leave_sheet_id": r[1].replace("\xa0", ""),
            "date": r[2],
            "instructors_comment": r[3],
            "leave_sections": [
                {"section": leave_list[0][index + 4], "reason": s}
                for index,s in enumerate(r[i:])
            ]
        }

        leave["leave_sections"] = list(
            filter(lambda x: x["reason"], leave["leave_sections"]))
        result.append(leave)
    return result


def submitLeave(session, start_date, end_date, leave_dict):
    """Submit leave data to leave.kaus.edu.tw:446
    session: The session include login cookies
    start_date: Start date for leave
    end_date: End date for leave
    leave_dict: A dict with data include which section were leave
        reason_id: String, 21 ~ 26.
        reason_text: String, a reason why leave.
        section: List, the number which count on it.

    return (success, value)
        success: Bool
        value: String
    """

    # First page
    r = session.get(SUBMIT_LEAVE_URL)

    root = etree.HTML(r.text)

    d = {i.attrib['name']: i.attrib['value'] for i in root.xpath("//input")}
    del d['ctl00$ButtonLogOut']

    # Setting start date and end date
    r = session.post(SUBMIT_LEAVE_URL, data=d)
    root = etree.HTML(r.text)

    d = {i.attrib['name']: i.attrib['value'] for i in root.xpath("//input[starts-with(@id, '__')]")}
    d["ctl00$ContentPlaceHolder1$CK001$DateUCCBegin$text1"] = start_date
    d["ctl00$ContentPlaceHolder1$CK001$DateUCCEnd$text1"] = end_date
    d["ctl00$ContentPlaceHolder1$CK001$ButtonCommit"] = u"下一步"

    # Setting leaving section
    r = session.post(SUBMIT_LEAVE_URL, data=d)
    root = etree.HTML(r.text)

    reason_map = {"21": u"事", "22": u"病", "23": u"公", "24": u"喪", "26": u"產"}

    # Setting reason id
    d = {i.attrib['name']: i.attrib['value'] for i in root.xpath("//input[starts-with(@id, '__')]")}
    d['ctl00$ContentPlaceHolder1$CK001$RadioButtonListOption'] = leave_dict[
        "reason_id"]
    d['ctl00$ContentPlaceHolder1$CK001$TextBoxReason'] = ""
    r = session.post(SUBMIT_LEAVE_URL, data=d)

    # Get Teacher id
    teacher_id = root.xpath("//option[@selected='selected']")[0].values()[-1]

    # Setting leaving button
    button = root.xpath(
        "//input[starts-with(@id, 'ContentPlaceHolder1_CK001_GridViewMain_Button_')]")

    for i in leave_dict["section"]:
        root = etree.HTML(r.text)
        d = {i.attrib['name']: i.attrib['value'] for i in root.xpath("//input[starts-with(@id, '__')]")}
        d['ctl00$ContentPlaceHolder1$CK001$RadioButtonListOption'] = leave_dict[
            "reason_id"]
        d['ctl00$ContentPlaceHolder1$CK001$TextBoxReason'] = leave_dict[
            'reason_text']
        d['ctl00$ContentPlaceHolder1$CK001$DropDownListTeacher'] = root.xpath(
            "//option[@selected='selected']")[0].values()[-1]
        d[button[int(i)].attrib['name']] = ''
        d['__ASYNCPOST'] = "ture"
        r = session.post(SUBMIT_LEAVE_URL, data=d)

    # Send to last step
    root = etree.HTML(r.text)
    d = {i.attrib['name']: i.attrib['value'] for i in root.xpath("//input[starts-with(@id, '__')]")}
    d['ctl00$ContentPlaceHolder1$CK001$TextBoxReason'] = leave_dict[
        'reason_text']
    d['ctl00$ContentPlaceHolder1$CK001$ButtonCommit2'] = "下一步"
    r = session.post(SUBMIT_LEAVE_URL, data=d)

    # Save leaving submit
    root = etree.HTML(r.text)
    d = {i.attrib['name']: i.attrib['value'] for i in root.xpath("//input[starts-with(@id, '__')]")}
    d['ctl00$ContentPlaceHolder1$CK001$ButtonSend'] = '存檔'
    files = {"ctl00$ContentPlaceHolder1$CK001$FileUpload1":
             (" ", "", "application/octet-stream")}

    # Send to server and save the submit
    r = session.post(SUBMIT_LEAVE_URL, files=files, data=d)
    root = etree.HTML(r.text)

    try:
        return_value = root.xpath("//script")[-1].text
        return_value = return_value[
            return_value.index('"') + 1: return_value.rindex('"')]
    except:
        return_value = "Error..."

    return_success = True if return_value == u'假單存檔成功，請利用假單查詢進行後續作業。' else False

    return (return_success, return_value)


if __name__ == '__main__':
    s = requests.session()
    login(s, "", "")
    #print(submitLeave(s, '103/09/25', '103/09/25', {"reason_id": "21", "reason_text": "testing", "section": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]}))
    # for test 
    # import json
    # print(json.dumps(getList(s,year='107',semester='1'),ensure_ascii=False))
