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
            "news_title": "文創CCI發報團隊 ─ 句句到味",
            "news_image": "http://i.imgur.com/IoVDFVA.jpg",
            "news_url": "https://www.facebook.com/whataboutcci",
            "news_content": "",
            "news_weight": 0
        },
        {
            "news_title": "2015 高應大校園歌唱大賽",
            "news_image": "http://i.imgur.com/lhBojIw.jpg",
            "news_url": "https://www.facebook.com/pages/2015%E9%AB%98%E6%87%89%E5%A4%A7%E6%A0%A1%E5%9C%92%E6%AD%8C%E5%94%B1%E5%A4%A7%E8%B3%BD/503404693131297?fref=ts",
            "news_content": "",
            "news_weight": 0
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
