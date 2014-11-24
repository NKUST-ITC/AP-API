# -*- coding: utf-8 -*-

ENABLE = 1
NEWS_ID = 8

news_image = ""

#            "正副會長候選人:<br>"
#            "1號候選人 — 呂紹榕 x 詹濬鍵<br>"
#            "2號候選人 — 江敬全 x 邱博雅<br><br>"
#            "以及18系正副會長,8系學生議員<br><br>"
#            "投票資格：日間部四技與日間部二技同學<br>"
#            "投票時間：早上10點至下午4點<br>"
#            "11/26(三):燕巢 - 管一室內廣場<br>"
#            "11/27(四):建工校區 - 中正堂<br>"

#"<div><img style='display:block;margin-left:auto;margin-right:auto;margin-bottom:-15px;max-width:100%;min-height:150px;height:auto;' src='"
#            + news_image + "'></img></div>"



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
   
    news_title = "不要投票"
    news_template = (
            "<div style='text-align:center;margin-top:-15px'>"
            "◎ 104級三合一選舉, DON'T VOTE ◎<br><br>"


            '<iframe width="100%" height="auto" src="//www.youtube.com/embed/KEQvBckPTXY" frameborder="0" allowfullscreen></iframe>'

        )
    news_url = "https://www.facebook.com/changekuas"


    return [ENABLE, NEWS_ID, news_title, news_template, news_url]