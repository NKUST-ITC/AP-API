#-*- encoding=utf-8

from lxml import etree
import requests

s = requests.session()

def login(session, username, password):
    root = etree.HTML(session.get("http://leave.kuas.edu.tw").text)
    
    form = {}
    for i in root.xpath("//input"):
        form[i.attrib['name']] = ""
        if "value" in i.attrib:
            form[i.attrib['name']] = i.attrib['value']

    form['Login1$UserName'] = username
    form['Login1$Password'] = password

    session.post('http://leave.kuas.edu.tw/', data=form )


def getList(session=s, year="102", semester="2"):
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


if __name__ == '__main__':
    login(s, "1102108133", "111")
    print(getList(s, "103", "1"))