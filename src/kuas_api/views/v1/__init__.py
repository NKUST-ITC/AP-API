# -*- coding: utf-8 -*-

import os
import json
from functools import wraps

import requests
import kuas_api.kuas.ap as ap
import kuas_api.kuas.user as user
import kuas_api.kuas.cache as cache

from flask import Flask, render_template, request, session, redirect
from flask_cors import *

from flask_apiblueprint import APIBlueprint


__version__ = "2.0"

android_version = "1.5.4"
android_donate_version = "2.0.0"
ios_version = "1.4.3"


api_v1 = APIBlueprint(
    'api_v1', __name__,
    subdomain='',
    url_prefix='')


def authenticate(func):
    @wraps(func)
    def call(*args, **kwargs):
        if 'c' in session:
            return func(*args, **kwargs)
        else:
            return "false"

    return call


def dump_cookies(cookies_list):
    """Dumps cookies to list
    """

    cookies = []
    for c in cookies_list:
        cookies.append({
            'name': c.name,
            'domain': c.domain,
            'value': c.value})

    return cookies


def set_cookies(s, cookies):
    for c in cookies:
        s.cookies.set(c['name'], c['value'], domain=c['domain'])


@api_v1.route('/')
def index():
    return "kuas-api version 1."


@api_v1.route('/version')
@cross_origin(supports_credentials=True)
def version():
    return android_version


@api_v1.route('/android_version')
@cross_origin(supports_credentials=True)
def a_version():
    return android_version


@api_v1.route('/android_donate_version')
@cross_origin(supports_credentials=True)
def a_donate_version():
    return android_donate_version


@api_v1.route('/ios_version')
@cross_origin(supports_credentials=True)
def i_version():
    return ios_version


@api_v1.route('/fixed')
@cross_origin(supports_credentials=True)
def is_fixed():
    return ""


@api_v1.route('/backup')
@cross_origin(supports_credentials=True)
def backup():
    return "0"


@api_v1.route('/status')
@cross_origin(supports_credentials=True)
def status():
    return json.dumps(cache.server_status())


@api_v1.route('/ap/semester')
@cross_origin(supports_credentials=True)
def ap_semester():
    semester_list = ap.get_semester_list()
    default_yms = list(filter(lambda x: x['selected'] == 1, semester_list))[0]
    return json.dumps({"semester": semester_list,
                       "default_yms": default_yms}, ensure_ascii=False)


@api_v1.route('/ap/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login_post():
    if request.method == "POST":
        session.permanent = True

        # Start login
        username = request.form['username']
        password = request.form['password']

        s = requests.session()
        is_login = cache.login(s, username, password)

        if is_login:
            # Serialize cookies with domain
            session['c'] = dump_cookies(s.cookies)
            session['username'] = username

            return "true"
        else:
            return "false"

    return render_template("login.html")


@api_v1.route('/ap/only/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def ap_login():
    if request.method == "POST":
        session.permanent = True

        # Start login
        username = request.form['username']
        password = request.form['password']

        s = requests.session()
        is_login = cache.ap.login(s, username, password)

        if is_login:
            # Serialize cookies with domain
            session['c'] = dump_cookies(s.cookies)
            session['username'] = username

            return "true"
        else:
            return "false"

    return render_template("login.html")


@api_v1.route('/ap/is_login', methods=['POST'])
@cross_origin(supports_credentials=True)
def is_login():
    if 'c' not in session:
        return "false"

    return "true"


@api_v1.route('/ap/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    session.clear()

    return 'logout'


@api_v1.route('/ap/query', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
@authenticate
def query_post():
    if request.method == "POST":
        fncid = request.form['fncid']
        arg01 = request.form['arg01'] if 'arg01' in request.form else None
        arg02 = request.form['arg02'] if 'arg02' in request.form else None
        arg03 = request.form['arg03'] if 'arg03' in request.form else None
        arg04 = request.form['arg04'] if 'arg04' in request.form else None

        # if 'c' not in session:
        #    return "false"
        # Restore cookies
        s = requests.session()
        set_cookies(s, session['c'])

        query_content = cache.ap_query(
            s, fncid, {"arg01": arg01, "arg02": arg02, "arg03": arg03, "arg04": arg04}, session['username'])

        if fncid == "ag222":
            return json.dumps(query_content)
        elif fncid == "ag008":
            return json.dumps(query_content)
        else:
            return json.dumps(query_content)

    return render_template("query.html")


@api_v1.route('/ap/user/info')
@cross_origin(supports_credentials=True)
@authenticate
def ap_user_info():
    # Restore cookies
    s = requests.session()
    set_cookies(s, session['c'])

    return json.dumps(user.get_user_info(s, session['username']))


@api_v1.route('/ap/user/picture')
@cross_origin(supports_credentials=True)
@authenticate
def ap_user_picture():
    # Restore cookies
    s = requests.session()
    set_cookies(s, session['c'])

    return user.get_user_picture(s, session['username'])


@api_v1.route('/leave', methods=["POST"])
@cross_origin(supports_credentials=True)
@authenticate
def leave_post():
    if request.method == "POST":
        print(request.form)
        arg01 = request.form['arg01'] if 'arg01' in request.form else None
        arg02 = request.form['arg02'] if 'arg02' in request.form else None

        # Restore cookies
        s = requests.session()
        set_cookies(s, session['c'])

        if arg01 and arg02:
            return json.dumps(cache.leave_query(s, arg01, arg02))
        else:
            return json.dumps(cache.leave_query(s))


@api_v1.route('/leave/submit', methods=['POST'])
@cross_origin(supports_credentials=True)
@authenticate
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
        return json.dumps((False, "請假維修中, 目前無法請假~"))

        # Fixed
        # if reason_id and reason_text and section:
        #    return json.dumps(cache.leave_submit(s, start_date, end_date, reason_id, reason_text, section))
        # else:
        #    return json.dumps((False, "Error..."))


@api_v1.route('/bus/query', methods=["POST"])
@cross_origin(supports_credentials=True)
@authenticate
def bus_query():
    if request.method == "POST":
        date = request.form['date']

        # Restore cookies
        s = requests.session()
        set_cookies(s, session['c'])

        return json.dumps(cache.bus_query(s, date))


@api_v1.route("/bus/reserve")
@cross_origin(supports_credentials=True)
@authenticate
def bus_reserve():
    if 'c' in session:
        s = requests.session()
        set_cookies(s, session['c'])

        return json.dumps(cache.bus_reserve_query(s))


@api_v1.route('/bus/booking', methods=["POST"])
@cross_origin(supports_credentials=True)
@authenticate
def bus_booking():
    if request.method == "POST":
        busId = request.form['busId']
        action = request.form['action']

        # Restore cookies
        s = requests.session()
        set_cookies(s, session['c'])

        return json.dumps(cache.bus_booking(s, busId, action))


@api_v1.route('/notification/<page>')
@cross_origin(supports_credentials=True)
def notification(page):
    page = int(page)
    return json.dumps(cache.notification_query(page))


@api_v1.route('/news')
@cross_origin(supports_credentials=True)
def news():
    return redirect("/v2/news")


@api_v1.route('/news/status')
@cross_origin(supports_credentials=True)
def news_status():
    return json.dumps(cache.news_status())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
