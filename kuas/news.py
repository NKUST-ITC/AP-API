# -*- coding: utf-8 -*-

ENABLE = 1
NEWS_ID = 25

NEWS_TITLE = "高應盃籃球錦標賽"
NEWS_IMAGE = "http://i.imgur.com/NAxVxbV.jpg"
NEWS_URL = "http://goo.gl/Yh1iIF"
NEWS_CONTENT = """
"""

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
   
    news_title = NEWS_TITLE
    news_template = (
            "<div style='text-align:center;'>"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;max-width:80%;min-height:150px;height:auto;' src='"
            + NEWS_IMAGE + "'></img>" + NEWS_CONTENT + "</div>" +
            "</div>"

        )
    news_url = NEWS_URL

    return [ENABLE, NEWS_ID, news_title, news_template, news_url]
