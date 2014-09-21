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

    news_title = ""
    news_template = (
            ""
        )
    news_url = ""


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]