# -*- coding: utf-8 -*-

ENABLE = 1
NEWS_ID = 5

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
   
    news_title = "活動消息"
    news_template = (
            "<div style='text-align:center;margin-top:-15px'>"
            "◎康委大冒險2-圖坦卡門之影◎<br><br>"
            "即將於本週禮拜四、五登場！<br>"
            "日期為：10/30、31日 晚上5～9點<br>"
            "可以當場換票 10張發票換一張門票<br><br>"
            "你準備好面對法老的冒險了嗎！"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;margin-bottom:-15px;max-width:100%;min-height:150px;height:auto;' src='http://i.imgur.com/SkevurF.jpg'></img></div>"
        )
    news_url = "https://www.facebook.com/ReliveIsland"


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]