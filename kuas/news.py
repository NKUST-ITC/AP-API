# -*- coding: utf-8 -*-

ENABLE = 1
NEWS_ID = 4

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
            "你,是否有勇氣深入危機四伏的金字塔內?<br>"
            "◎康委大冒險2-圖坦卡門之影◎<br>"
            "排票日期：<br><hr>"
            "燕巢場10/16（四）下午12點～3點<br>管一室內廣場<br><hr>"
            "建功場10/18（六）下午1點～5點<br>咖廣<br>"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;margin-bottom:-15px;max-width:100%;min-height:150px;height:auto;' src='http://i.imgur.com/SkevurF.jpg'></img></div>"
        )
    news_url = "https://www.facebook.com/ReliveIsland"


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]