# -*- coding: utf-8 -*-

import random

ENABLE = 1
NEWS_ID = 26

NEWS_TITLE = ""
NEWS_IMAGE = "http://i.imgur.com/NAxVxbV.jpg"
NEWS_URL = "http://goo.gl/Yh1iIF"
NEWS_CONTENT = """
"""

def random_news():
    news_list = [
        {
            "news_title": "高應盃籃球錦標賽",
            "news_image": "http://i.imgur.com/NAxVxbV.jpg",
            "news_url": "http://goo.gl/Yh1iIF",
            "news_content": ""
        }, 

        {
            "news_title": "應外 News 起來",
            "news_image": "http://i.imgur.com/sVMvNhr.jpg",
            "news_url": "https://www.facebook.com/AFLDEARS",
            "news_content": """
            應外Nova News 讓你春風滿面 前無古人 全新活動<br>
            3/30 隆重登場！
            """
        }
    ]


    return random.choice(news_list)


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
   
    # Get news from random news
    news = random_news()

    news_title = news["news_title"]
    news_template = (
            "<div style='text-align:center;'>"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;max-width:80%;min-height:150px;height:auto;' src='"
            + news["news_image"] + "'></img>" + news["news_content"] + "</div>" +
            "</div>"

        )
    news_url = news["news_url"]

    return [ENABLE, NEWS_ID, news_title, news_template, news_url]
