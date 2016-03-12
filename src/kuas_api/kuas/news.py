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
            "news_title": "第八屆泰北團-夢想，「泰」不一樣",
            "news_image": "http://i.imgur.com/iNbbd4B.jpg",
            "news_url": "https://docs.google.com/forms/d/11Awcel_MfPeiEkl7zQ0MldvnAw59gXKLecbIODPOaMs/viewform?edit_requested=true",
            "news_content": "",
            "news_weight": 3
        },
        {
            "news_title": "體委幹部體驗營",
            "news_image": "http://i.imgur.com/aJyQlJp.jpg",
            "news_url": "https://www.facebook.com/Kuas%E9%AB%94%E5%A7%94-440439566106678/?fref=ts",
            "news_content": "",
            "news_weight": 4
        },
        {
            "news_title": "遊戲外掛 原理實戰",
            "news_image": "http://i.imgur.com/WkI23R2.jpg",
            "news_url": "https://www.facebook.com/profile.php?id=735951703168873",
            "news_content": "",
            "news_weight": 6
        },
        {
            "news_title": "好日子育樂營",
            "news_image": "https://scontent-hkg3-1.xx.fbcdn.net/hphotos-xft1/v/t34.0-0/p206x206/12834566_977348362345349_121675822_n.jpg?oh=e04f6830fdfe5d3a77e05a8b3c32fefc&oe=56E663E6",
            "news_url": "https://m.facebook.com/kuasYGR/",
            "news_content": "",
            "news_weight": 6
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
