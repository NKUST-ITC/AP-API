# -*- coding: utf-8 -*-
import time
import json
from flask import request, g
from flask_cors import *
import kuas_api.kuas.cache as cache

from kuas_api.modules.stateless_auth import auth
import kuas_api.modules.stateless_auth as stateless_auth
import kuas_api.modules.error as error
from kuas_api.modules.json import jsonify
from .doc import auto


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


@route('/bus/timetables')
@auto.doc(groups=["public"])
#@cross_origin(supports_credentials=True)
@auth.login_required
def timetables():
    """Get KUAS school bus time table.

    :query string date: Specific date to query timetable. format: yyyy-mm-dd
    :query string from: The start station you want to query. (not impl yet)
    :statuscode 200: no error


    **Requires authentication?**

      Yes

    **Request**

    without date (default the date on server)

    .. sourcecode:: http

        GET /latest/bus/timetables HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -i -X GET localhost:8001/v2/bus/timetables

    with date

    .. sourcecode:: http

        GET /latest/bus/timetables?date=2015-9-1 HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=


    **Response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
          "timetable":[
            {
              "endStation":"燕巢",
              "EndEnrollDateTime":"2015-08-31 17:20",
              "isReserve":-1,
              "Time":"08:20",
              "busId":"27034",
              "limitCount":"999",
              "reserveCount":"27",
              "runDateTime":"2015-09-01 08:20"
            },
            {
              "endStation":"燕巢",
              "EndEnrollDateTime":"2015-09-01 08:00",
              "isReserve":-1,
              "Time":"13:00",
              "busId":"27062",
              "limitCount":"999",
              "reserveCount":"1",
              "runDateTime":"2015-09-01 13:00"
            },
            {
              "endStation":"建工",
              "EndEnrollDateTime":"2015-09-01 07:15",
              "isReserve":-1,
              "Time":"12:15",
              "busId":"27090",
              "limitCount":"999",
              "reserveCount":"5",
              "runDateTime":"2015-09-01 12:15"
            },
            {
              "endStation":"建工",
              "EndEnrollDateTime":"2015-09-01 11:45",
              "isReserve":-1,
              "Time":"16:45",
              "busId":"27118",
              "limitCount":"999",
              "reserveCount":"24",
              "runDateTime":"2015-09-01 16:45"
            }
          ],
          "date":"2015-9-1"
        }

    """

    date = time.strftime("%Y-%m-%d", time.gmtime())
    if request.args.get("date"):
        date = request.args.get("date")

    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    return jsonify(date=date, timetable=cache.bus_query(s, date))


@route("/bus/reservations", methods=["GET"])
@route("/bus/reservations/<int:bus_id>", methods=["PUT"])
@route("/bus/reservations/<int:cancel_key>", methods=["DELETE"])
@auth.login_required
def bus_reservations(bus_id=None, cancel_key=None):
    """
    .. warning::

      This endpoints is still under construct,
      return value `may` change quickly.

      Please check this documentations for update.


    .. http:get:: /bus/reservations

      Get user's bus reservation.

      **Requires authentication?**

        Yes

      **Request**

        .. sourcecode:: http

      **Response**

        .. sourcecode:: http


    .. http:put:: /bus/reservations

        put

    .. http:delete:: /bus/reservations

        delete
    """

    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    # Debugging
    user_agent = request.user_agent.string
    user_id = g.username

    if request.method == "GET":
        return jsonify(reservation=cache.bus_reserve_query(s))
    elif request.method == "PUT":
        result = cache.bus_booking(s, bus_id, "")

        print("PUT,%s,%s,%s" % (user_agent, user_id, result))

        return jsonify(result)
    elif request.method == "DELETE":
        result = cache.bus_booking(s, cancel_key, "un")

        print("DELETE,%s,%s,%s" % (user_agent, user_id, result))

        return jsonify(result)



    return request.method
