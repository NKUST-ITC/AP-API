# -*- coding: utf -*-

import requests
from lxml import etree


def get_admin_calendar(year, semester):
    data = {
        "ContentPlaceHolder1_ToolkitScriptManager1_HiddenField": ";;AjaxControlToolkit,+Version=4.1.60919.0,+Culture=neutral,+PublicKeyToken=28f01b0e84b6d53e:zh-TW:ee051b62-9cd6-49a5-87bb-93c07bc43d63:de1feab2:f9cec9bc:a0b0f951:a67c2700:fcf0e993:f2c8e708:720a52bf:589eaa30:698129cf:fb9b4c57:ccb96cf9",
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "ContentPlaceHolder1_TabContainer1_ClientState": '{"ActiveTabIndex":1,"TabEnabledState":[true,true,true,true,true],"TabWasLoadedOnceState":[true,true,false,false,false]}',
        "__LASTFOCUS": "",
        "__VIEWSTATE": "/wEPDwUKMTI1OTYxMzEwMA8WAh4XRGVmYXVsdFNjaFllYXJTZW1TdHJpbmcFBTEwMy0yFgJmD2QWAgIED2QWAgIBD2QWBgIBD2QWAgIBD2QWBAIBDw8WAh4HVmlzaWJsZWhkFgQCAw8PFgIeBFRleHQFD+iri+i8uOWFpeW4s+iZn2RkAgcPDxYEHgRNb2RlCyolU3lzdGVtLldlYi5VSS5XZWJDb250cm9scy5UZXh0Qm94TW9kZQAfAgUP6KuL6Ly45YWl5a+G56K8ZGQCAw8PFgIfAWdkFgQCAQ8PFgIfAgUZ5Zub6LOH5bel5LiJ55SyLeWRgue0ueamlWRkAgMPDxYCHwIFHeatoei/juS9v+eUqCDmpa3li5nooYzkuovmm4YhZGQCAw9kFgICAQ88KwANAQwUKwACBQcyOjAsMDowFCsAAhYEHwIFD+alreWLmeihjOS6i+abhh4FVmFsdWUFD+alreWLmeihjOS6i+abhmQWAmYPZBYCZg8VAQ/mpa3li5nooYzkuovmm4ZkAgUPZBYCAgEPZBYCAgEPZBYCAgMPDxYEHghUYWJJbmRleAEAAB4STGFzdEFjdGl2ZVRhYkluZGV4AgFkFgZmD2QWAmYPZBYCAgEPZBYEAgEPEA8WBh4NRGF0YVRleHRGaWVsZAUQU2NoWWVhclNlbVN0cmluZx4ORGF0YVZhbHVlRmllbGQFD1NjaFllYXJTZW1WYWx1ZR4LXyFEYXRhQm91bmRnZBAVBAcxMDQg5LiLBzEwNCDkuIoHMTAzIOS4iwcxMDMg5LiKFQQFMTA0LTIFMTA0LTEFMTAzLTIFMTAzLTEUKwMEZ2dnZ2RkAgcPZBYCAgEPFgIeA3NyYwVRaHR0cDovL2FjdGl2ZS5rdWFzLmVkdS50dy9FUG9ydGZvbGlvL0FjdGl2aXR5L0RvY3VtZW50L0JzL0NhbGVuZGFyL0JzXzEwMy3kuIsucGRmZAIBD2QWAmYPZBYCAgEPZBYEAgEPEA8WBh8HBRBTY2hZZWFyU2VtU3RyaW5nHwgFD1NjaFllYXJTZW1WYWx1ZR8JZ2QQFQQHMTA0IOS4iwcxMDQg5LiKBzEwMyDkuIsHMTAzIOS4ihUEBTEwNC0yBTEwNC0xBTEwMy0yBTEwMy0xFCsDBGdnZ2dkZAIDDxAPFgYfBwUKdXBVbml0TmFtZR8IBQh1cFVuaXRpZB8JZ2QQFRMM5YWo6YOo6aGv56S6CeaVmeWLmeiZlQnkuLvoqIjlrqQP6YCy5L+u5o6o5buj6JmVDOmAsuS/ruWtuOmZognnuL3li5nomZUY55Kw5aKD5a6J5YWo6KGb55Sf5Lit5b+DGOioiOeul+apn+iIh+e2sui3r+S4reW/gwnlnJbmm7jppKgJ5Lq65LqL5a6kCemrlOiCsuWupAzlia/moKHplbflrqQJ56CU55m86JmVD+Wci+mam+S6i+WLmeiZlRjmoKHlj4voga/ntaHogbfmtq/kuK3lv4MJ5a245YuZ6JmVCeenmOabuOWupBLpgJrorZjmlZnogrLkuK3lv4MP54eV5bei5qCh5YuZ6YOoFRMBQQRBQTAwBEFDMDAEQUUwMARBVDAwBEdBMDAER0IwMARJQzAwBExCMDAEUEUwMARQSDAwBFBTMDAEUkEwMARSQjAwBFJEMDAEU0EwMARTRTAwBFhDMDAEWUQwMBQrAxNnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCBA9kFgJmD2QWAgIBD2QWDAIFDxBkZBYBZmQCBw8QZGQWAGQCEQ9kFgICBQ9kFgQCAQ8QZGQWAQIIZAIDDxBkZBYBZmQCEw9kFgICBQ9kFgQCAQ8QZGQWAQIIZAIDDxBkZBYBZmQCFQ8PFgIfAgUS5qWt5YuZ5rS75YuV5p+l6KmiZGQCGQ88KwARAQEQFgAWABYAZBgDBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUnY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRUYWJDb250YWluZXIxBSdjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJFRhYkNvbnRhaW5lcjEPD2QCAWQFTGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkVGFiQ29udGFpbmVyMSRUYWJQYW5lbEJzU2VhcmNoJGd2Rm9yQnNBY3RpdmVTZWFyY2gPZ2RyQEeUQZjPVmQxmQjXEE2h5a2Akm5FOox6NGaKCQuRSg==",
        "__EVENTVALIDATION": "/wEWNQLQjpnOBwLe9pSEBwLRovlJAqCG2dcHAqGG2dcHAr/xv7kNArzxv7kNAueA6J4LAtqnpbUMAoaIxIIDAoeIxIIDApn/ouwJApr/ouwJAoOR2+EEAqXQ+IUIAqXQ8IUIAqXQiIYIAqXQzIUIAq/Q+IUIAq/Q9IUIAt3R8IUIAqLQ9IUIAtbRiIYIAtbR3IUIAtbRsIUIAtTR+IUIAtTR9IUIAtTRjIYIAtvR+IUIAtvRiIYIAs7R8IUIAs3RjIYIApW90PwFAuKa6aQNAoWPzooGAqzGkOoMAreinuYKAtSP93EC0pDX/QEC9czo6g0ChJvWOwKOnbn6BALd9PzVDALm9IzLDAKV0ZqFCQLswvqaBgKNu8fRDwKH9+z4CAKM5rDmAQLrtJjFBALpvue2BwLE4euUCQKVtruvDVM6q8J60kK+Rs+JNbFQOsCQU/juUwZnaTkYwDCI5LJO",
        "ctl00$ContentPlaceHolder1$TabContainer1$TabPanelBs$DropDownListForBsFormalSchYearSem": "103-2",
        "ctl00$ContentPlaceHolder1$TabContainer1$TabPanelBsGov$DropDownListForBsGovSchYearSem": "104-1",
        "ctl00$ContentPlaceHolder1$TabContainer1$TabPanelBsGov$DropDownListForBsGovUnit": "A",
        "ctl00$ContentPlaceHolder1$TabContainer1$TabPanelBsGov$ButtonSearchForBsGov": "查詢",
        "ctl00$ContentPlaceHolder1$TabContainer1$TabPanelBsSearch$TextBoxForKeyword": "",
        "ctl00$ContentPlaceHolder1$TabContainer1$TabPanelBsSearch$DDLForGovOrTeach": "選擇部門",
        "ctl00$ContentPlaceHolder1$TabContainer1$TabPanelBsSearch$DateTimeBoxForStart$DateFieldBox": "2015/9/11",
        "ctl00$ContentPlaceHolder1$TabContainer1$TabPanelBsSearch$DateTimeBoxForEnd$DateFieldBox": "2015/9/11",
    }

    cookies = {
        '_ga': 'GA1.3.518100922.1435057856',
        'ASP.NET_SessionId': 'jyeffb1tbujhgzju0mpclnaz',
        '_gat': '1',
    }

    headers = {
        'Host': 'active.kuas.edu.tw',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.7,zh-TW;q=0.3',
        'Referer': 'http://active.kuas.edu.tw/EPortfolio/Activity/UnitBsCalendar.aspx',
        'Connection': 'keep-alive',
    }

    r = requests.post('http://active.kuas.edu.tw/EPortfolio/Activity/UnitBsCalendar.aspx', headers=headers, cookies=cookies, data=data)

    f = open("/tmp/test", "w")
    f.write(r.text)

    root = etree.HTML(r.text)
    root.xpath("id('ContentPlaceHolder1_TabContainer1_TabPanelBsGov_TDContent_109')")[0].xpath("a")[7].values()


if __name__ == "__main__":
    pass
    #get_admin_calendar(104, 1)
