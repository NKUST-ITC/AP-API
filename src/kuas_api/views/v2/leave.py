# -*- coding: utf-8 -*-
import json
import requests

from flask import request, g
from flask_cors import *

import kuas_api.kuas.cache as cache

from kuas_api.modules.stateless_auth import auth
import kuas_api.modules.stateless_auth as stateless_auth
import kuas_api.modules.const as const
from kuas_api.modules.json import jsonify


from .doc import auto

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


@route('/leaves/<int:year>/<int:semester>')
@auth.login_required
def get_leave(year, semester):
    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    leaves = cache.leave_query(s, year, semester)

    if not leaves:
        return jsonify(status=const.no_content, messages="本學期無缺曠課記錄", leaves=[])
    else:
        return jsonify(status=const.ok, messages="", leaves=leaves)


@route('/leave/submit', methods=['POST'])
@auto.doc()
@cross_origin(supports_credentials=True)
@auth.login_required
def leave_submit():
    if request.method == 'POST':
        start_date = request.form['start_date'].replace("-", "/")
        end_date = request.form['end_date'].replace("-", "/")
        reason_id = request.form[
            'reason_id'] if 'reason_id' in request.form else None
        reason_text = request.form[
            'reason_text'] if 'reason_text' in request.form else None
        section = json.loads(
            request.form['section']) if 'section' in request.form else None

        s = requests.session()
        set_cookies(s, session['c'])

        start_date = start_date.split("/")
        start_date[0] = str(int(start_date[0]) - 1911)
        start_date = "/".join(start_date)

        end_date = end_date.split("/")
        end_date[0] = str(int(end_date[0]) - 1911)
        end_date = "/".join(end_date)

        # Fixing, don't send it
        return json.dumps((False, "請假維修中, 目前無法請假~"), ensure_ascii=False)

        # Fixed
        # if reason_id and reason_text and section:
        #    return json.dumps(cache.leave_submit(s, start_date, end_date, reason_id, reason_text, section))
        # else:
        #    return json.dumps((False, "Error..."))
