# -*- coding: utf-8 -*-
import time
import json
from flask import jsonify
from flask_cors import *
import kuas_api.kuas.cache as cache

from kuas_api.modules.stateless_auth import auth
import kuas_api.modules.stateless_auth as stateless_auth
import kuas_api.modules.error as error
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
@cross_origin(supports_credentials=True)
@auth.login_required
def timetables():
    """Get KUAS school bus time table.
    """

    date = time.strftime("%Y-%m-%d", time.gmtime())
    if request.args.get("date"):
        date = request.args.get("date")

    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    return json.dumps(cache.bus_query(s, date), ensure_ascii=False)


@route("/bus/reservations", methods=["GET"])
@route("/bus/reservations/<int:bus_id>", methods=["PUT"])
@route("/bus/reservations/<string:end_time>", methods=["DELETE"])
@auto.doc(groups=["public", "GET", "PUT", "DELETE"])
@cross_origin(supports_credentials=True)
@auth.login_required
def bus_reservations(bus_id=None, end_time=None):
    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    if request.method == "GET":
        return json.dumps(cache.bus_reserve_query(s), ensure_ascii=False)
    elif request.method == "PUT":
        return json.dumps(cache.bus_booking(s, bus_id, ""), ensure_ascii=False)
    elif request.method == "DELETE":
        return json.dumps(cache.bus_booking(s, end_time, "un"), ensure_ascii=False)

    return request.method
