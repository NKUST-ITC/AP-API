#-*- encoding=utf-8

from lxml import etree
import requests


NOTIFICATION_URL = "http://www.kuas.edu.tw/files/501-1000-1003-%d.php"

def get(page=1):
    r = requests.get(NOTIFICATION_URL %(page))
    r.encoding = "utf-8"

    root = etree.HTML(r.text)
    trs = root.xpath("//tr[starts-with(@class, 'row')]")

    result = []
    for tr in trs:
        a = tr.xpath("td//a")[0].values()[0]
        tr = list(filter(lambda x: x, map(lambda x: x.replace("\t", "").replace("\n", ""), tr.itertext())))
        tr = tr[1:]

        result.append({'link': a, 'info': tr})

    return result

if __name__ == "__main__":
    print(get(2))
