# -*- coding: utf-8 -*-

import random

ENABLE = 1
NEWS_ID = 30


def random_news():
    news_list = [
       	{
            "news_title": "你的網路安全嗎？",
            "news_image": "http://i.imgur.com/bQ3fCzo.jpg",
            "news_url": "https://www.facebook.com/KUASITC/posts/750663035031073",
            "news_content": ""
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
