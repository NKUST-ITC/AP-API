# -*- coding: utf-8 -*-

ENABLE = 1
NEWS_ID = 21

news_image = "http://a2.mzstatic.com/us/r30/Purple3/v4/2b/5b/c9/2b5bc980-341f-bf30-ed07-e14b1d009575/icon175x175.jpeg"
news_content = """
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
   
    news_title = "iOS 版更新"
    news_template = (
            "<div style='text-align:center;margin-top:-15px'>"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;margin-bottom:-15px;max-width:100%;min-height:150px;height:auto;' src='"
            + news_image + "'></img></div>"
            + news_content +
            "</div>"

        )
    news_url = "itms-apps://itunes.com/apps/gao-ying-xiao-wu-tong/"


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]
