# -*- coding: utf-8 -*-

ENABLE = 1
NEWS_ID = 2

def news_status():
    return [ENABLE, NEWS_ID]

def news():
    """
    News for kuas.

    return [enable, news_id, news_title, news_template, news_url]
        enable: bool
        news_id: int
        news_title: string
        news_tempalte: string
        news_url: string
    """
   
    """
    news_title = "活動消息"
    news_template = (
            "<div style='text-align:center;margin-top:-15px'>"
            "睽違了一年 今年的大冒險再度啟航啦!!<br>"
            "你,是否有勇氣深入危機四伏的金字塔內?<br><br>"
            "◎康委大冒險2-圖坦卡門之影◎<br><br>"
            "活動日：10/30、10/31<br>活動地點：高應大中正堂<br>活動時間：17:00~21:00</div>"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;margin-bottom:-15px;max-width:100%;min-height:150px;height:auto;' src='http://i.imgur.com/SkevurF.jpg'></img></div>"
        )
    news_url = "https://www.facebook.com/ReliveIsland"
    """

    news_title = "停電公告"
    news_template = (
            "<div style='text-align:center;margin-top:-15px;margin:0 auto;width:85%;'>"
            "因10月10日(五)計網中心全機房斷電,新增不斷電系統與數位電表。<br><br>"
            "故10月10日當天校車預約系統無法預約交通車。<br><br>"
            "請有要預約10月10日交通車的師生，在<font color='red'>10月9日中午12點前</font>上校車預約系統預約，以避免沒有校車可搭乘."
            "</div>"
            )
    news_url = ""

    return [ENABLE, NEWS_ID, news_title, news_template, news_url]
