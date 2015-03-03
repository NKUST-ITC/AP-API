# -*- coding: utf-8 -*-

ENABLE = 1
NEWS_ID = 22

news_image = "https://lh4.googleusercontent.com/1IswTw-BwsJZCsZU8uY-WDdHaaoHEQFdcdp4NADWMyUmC9D6yZp_52NQP96UZMrkWP97Og"
news_content = """<br><br>
3月4日（三）開始<br>
每日中午12:00~13:30<br>
建工龍捲風廣場及燕巢館一候車處皆會有我們的身影!<br><br>
歡迎現場預購帽T
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
   
    news_title = "高應帽T現場預購!"
    news_template = (
            "<div style='text-align:center;margin-top:-15px'>"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;margin-bottom:-15px;max-width:100%;min-height:150px;height:auto;' src='"
            + news_image + "'></img>" + news_content + "</div>" +
            "</div>"

        )
    news_url = "https://www.facebook.com/pages/%E6%87%89%E6%88%91%E5%80%91%E7%9A%84%E5%B8%BD%E8%B8%A2-KUAS-Exclusive-Hoodies/1439431772983278?fref=ts"


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]
