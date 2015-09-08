# -*- coding: utf-8 -*-
import json

from flask import request, g
from flask_cors import *

import kuas_api.kuas.ap as ap
import kuas_api.kuas.user as user
import kuas_api.kuas.cache as cache

from kuas_api.modules.json import jsonify
from kuas_api.modules.stateless_auth import auth
import kuas_api.modules.stateless_auth as stateless_auth
import kuas_api.modules.error as error


# Nestable blueprints problem
# not sure isn't this a best practice now.
# https://github.com/mitsuhiko/flask/issues/593
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


@route('/ap/users/info')
@auth.login_required
def ap_user_info():
    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    return json.dumps(user.get_user_info(s), ensure_ascii=False)


@route('/ap/users/picture')
@auth.login_required
def ap_user_picture():
    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    return user.get_user_picture(s)


@route('/ap/semester')
def ap_semester():
    semester_list = ap.get_semester_list()
    default_yms = list(
        filter(lambda x: x['selected'] == 1, semester_list))[0]

    # Check default args
    if request.args.get("default") == "1":
        return jsonify(default=default_yms)

    # Check limit args
    limit = request.args.get("limit")
    if limit:
        try:
            semester_list = semester_list[: int(limit)]
        except ValueError:
            return error.error_handle(
                status=400,
                developer_message="Error value for limit.",
                user_message="You type a wrong value for limit.")

    return jsonify(
        semester=semester_list,
        default=default_yms
    )


@route('/ap/query')
@auth.login_required
def query_post():
    fncid = request.form['fncid']
    arg01 = request.form['arg01'] if 'arg01' in request.form else None
    arg02 = request.form['arg02'] if 'arg02' in request.form else None
    arg03 = request.form['arg03'] if 'arg03' in request.form else None
    arg04 = request.form['arg04'] if 'arg04' in request.form else None

    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    query_content = cache.ap_query(
        s, fncid, {"arg01": arg01, "arg02": arg02, "arg03": arg03, "arg04": arg04}, g.username)

    if fncid == "ag222":
        return json.dumps(query_content)
    elif fncid == "ag008":
        return json.dumps(query_content)
    else:
        return json.dumps(query_content)
