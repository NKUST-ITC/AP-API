# -*- coding: utf-8 -*-

ENABLE = 1
NEWS_ID = 7

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
   
    news_title = "三合一選舉"
    news_template = (
            "<div style='text-align:center;margin-top:-15px'>"
            "◎104級三合一選舉學生會正副會長候選人政見發表會 - 逐字稿◎<br><br>"
            "1號候選人 — 呂紹榕 x 詹濬鍵<br>"
            "2號候選人 — 江敬全 x 邱博雅<br><br>"
            "錯過了正副會長政見發表會<br>想要了解兩組候選人說了些什麼嗎？<br><br>"
            "點選立即前往，透過逐字稿<br>了解兩組候選人的政見吧！"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;margin-bottom:-15px;max-width:100%;min-height:150px;height:auto;' src='http://i.imgur.com/YsV56MB.png'></img></div>"
        )
    news_url = "http://goo.gl/5ozyWe"


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]