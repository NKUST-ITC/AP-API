# -*- coding: utf-8 -*-

ENABLE = 0
NEWS_ID = 0

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


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]