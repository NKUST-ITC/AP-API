# -*- coding: utf-8 -*-

import kuas_api.kuas.cache as cache

from kuas_api.modules.json import jsonify


# Nestable blueprints problem
# not sure isn't this a best practice now.
# https://github.com/mitsuhiko/flask/issues/593
#from kuas_api.views.v2 import api_v2
routes = []


def route(rule, **options):
    def decorator(f):
        url_rule = {
            "rule": rule,
            "view_func": f,
            "options": options if options else {}
        }

        routes.append(url_rule)
        return f

    return decorator


@route('/notifications/<int:page>')
def notification(page):
    """Get KUAS notification

    :param int page: specific page for notifications


    **Request**

        .. sourcecode:: http

            GET /v2/notifications/1 HTTP/1.1
            Host: https://kuas.grd.idv.tw:14769/v2/notifications/1

        .. sourcecode:: shell

            curl -X GET https://kuas.grd.idv.tw:14769/v2/notifications/1

    **Response**

        .. sourcecode:: http

            HTTP/1.0 200 OK
            Content-Type: application/json


            {
              "page":1,
              "notification":[
                {
                  "link":"http://student.kuas.edu.tw/files/13-1002-45032-1.php",
                  "info":{
                    "title":"『鄭豐喜國外深造獎助學金』104年度申請辦法公告",
                    "date":"2015-09-04 ",
                    "id":"1",
                    "department":"諮商輔導中心"
                  }
                },
                {
                  "link":"http://gender.kuas.edu.tw/files/13-1005-45026-1.php",
                  "info":{
                    "title":"轉知社團法人台灣愛之希望協會辦理-104年同志公民運動系列活動，歡迎踴躍參加。",
                    "date":"2015-09-04 ",
                    "id":"2",
                    "department":"性別平等專區"
                  }
                },
                {},
                {}
              ]
            }
    """

    return jsonify(
        page=page,
        notification=cache.notification_query(page)
    )
