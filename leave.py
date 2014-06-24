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

    # Just abort class C to 14
    # And row id, leave id, teacher quote
    for r in tr:
        r = list(map(lambda x: x.replace("\r", "").
        						replace("\n", "").
                                replace("\t", "").
                                replace(u"\u3000", "").
                                replace(" ", ""),
                        r.itertext()
                        ))

        if not r[0]: del r[0]
        if not r[-1]: del r[-1]

        r = r[2: -5]
        del r[1]

        # Teacher quote

        result.append(r)

    return result


if __name__ == '__main__':
    login(s, "1102108133", "111")
    print(getList(s))
