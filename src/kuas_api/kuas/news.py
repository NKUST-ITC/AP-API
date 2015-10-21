# -*- coding: utf-8 -*-

import random

ENABLE = 1
NEWS_ID = 31
NEWS_DEBUG = False

DEFAULT_WEIGHT = 10


def random_by_weight(p):
    choice_id = []
    for i in range(len(p)):
        choice_id += [i for _ in range(DEFAULT_WEIGHT + p[i]["news_weight"])]

    return p[random.choice(choice_id)]


def random_news():
    news_list = [
        {
            "news_title": "流浪拼圖 Puzzles of wander",
            "news_image": "http://i.imgur.com/NzYCzY4.jpg",
            "news_url": "https://www.facebook.com/Puzzlesofwander",
            "news_content": "",
            "news_weight": 4
        },

        {
            "news_title": "觀光-航空走秀",
            "news_image": "http://i.imgur.com/OzrJIZZ.jpg",
            "news_url": "https://www.facebook.com/2014TMATOPSHOW",
            "news_content": "",
            "news_weight": 4
        },
        {
            "news_title": "資安爐邊聚會",
            "news_image": "http://i.imgur.com/BpxTSlC.png",
            "news_url": "http://kuas-it.kktix.cc/events/2015-talk-1",
            "news_content": "",
            "news_weight": 8
        },
        {
            "news_title": "眼界陸-晚安電影院",
            "news_image": "http://i.imgur.com/gnBbsSM.jpg",
            "news_url": "https://www.facebook.com/ScopeFilmFestival?__mref=message_bubble",
            "news_content": "",
            "news_weight": 3
        },
        {
            "news_title": "去你的文創節",
            "news_image": "http://i.imgur.com/G6C2kwm.jpg",
            "news_url": "https://www.facebook.com/I.LIKE.CCI",
            "news_content": "",
            "news_weight": 5
        }
    ]

    if NEWS_DEBUG:
        return news_list[0]
    else:
        return random_by_weight(news_list)


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
