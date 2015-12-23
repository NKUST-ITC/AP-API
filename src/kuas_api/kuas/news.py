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
            "news_title": "第八屆搖音新生盃",
            "news_image": "http://i.imgur.com/ziFEckz.jpg",
            "news_url": "https://www.facebook.com/KUAS.RockMusicCompany/photos/pb.240024276068437.-2207520000.1446562914./945089888895202/?type=3&theater",
            "news_content": "",
            "news_weight": 4
        },
        {
            "news_title": "期末成果發表會 [春韻]",
            "news_image": "http://i.imgur.com/To8vitb.jpg",
            "news_url": "https://www.facebook.com/events/806882852767987/",
            "news_content": "",
            "news_weight": 4
        },
        {
            "news_title": "我的藝響實驗舞臺-藝起來藝文活動",
            "news_image": "http://i.imgur.com/eLbq9KU.jpg",
            "news_url": "https://www.facebook.com/kuasfunart/?pnref=story&__mref=message_bubble",
            "news_content": "",
            "news_weight": 4
        },
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
