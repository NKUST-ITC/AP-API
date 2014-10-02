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

    news_title = "活動消息"
    news_template = (
            "<div style='text-align:center;margin-top:-15px'>"
            "睽違了一年 今年的大冒險再度啟航啦!!<br>"
            "你,是否有勇氣深入危機四伏的金字塔內?<br><br>"
            "◎康委大冒險2-圖坦卡門之影◎<br><br>"
            "活動日：10/30、10/31<br>活動地點：高應大中正堂<br>活動時間：18:00~22:00</div>"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;margin-bottom:-15px;max-width:100%;min-height:180px;height:auto;' src='https://fbcdn-sphotos-h-a.akamaihd.net/hphotos-ak-xpa1/v/t34.0-12/s180x540/10634199_778926775498920_832242890_n.jpg?oh=71b544273f86732afdef098ff6929607&oe=542ECBC9&__gda__=1412411491_15f9688f6755a7c91a5e57233fcc8443'></img></div>"
        )
    news_url = "https://www.facebook.com/ReliveIsland"


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]