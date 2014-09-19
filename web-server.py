# -*- coding: utf-8 -*-

import os
import json
import requests
import uniout
import kuas.parse as parse
import kuas.function as function

from flask import Flask, render_template, request, session
from flask_cors import *

__version__ = "1.4.0 leave"

android_version = "1.4.1"
android_donate_version = "1.4.1"
ios_version = "1.3.2"

app = Flask(__name__)
app.config.from_object("config")


def dump_cookies(cookies_list):
    cookies = []
    for c in cookies_list:
        cookies.append({
            'name': c.name,
            'domain': c.domain,
            'value': c.value
            })

    return cookies


def set_cookies(s, cookies):
    for c in cookies:
        s.cookies.set(c['name'], c['value'], domain=c['domain'])
        

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/version')
@cross_origin(supports_credentials=True)
def version():
    return android_version


@app.route('/android_version')
@cross_origin(supports_credentials=True)
def a_version():
    return android_version


@app.route('/android_donate_version')
@cross_origin(supports_credentials=True)
def a_donate_version():
    return android_donate_version


@app.route('/ios_version')
@cross_origin(supports_credentials=True)
def i_version():
    return ios_version


@app.route('/fixed')
@cross_origin(supports_credentials=True)
def is_fixed():
    return ""


@app.route('/backup')
@cross_origin(supports_credentials=True)
def backup():
    return "0"


@app.route('/status')
@cross_origin(supports_credentials=True)
def status():
    return json.dumps(function.server_status())


@app.route('/ap/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login_post():
    if request.method == "POST":
        session.permanent = True

        # Start login
        username = request.form['username']
        password = request.form['password']
        
        s = requests.session()
        is_login = function.login(s, username, password)

        if is_login:
            # Serialize cookies with domain 
            session['c'] = dump_cookies(s.cookies)

            return "true"
        else:
            return "false"


    return render_template("login.html")


@app.route('/ap/is_login', methods=['POST'])
@cross_origin(supports_credentials=True)
def is_login():
    if 'c' not in session :
        return "false"

    return "true"


@app.route('/ap/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    session.clear()

    return 'logout'


@app.route('/ap/query', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def query_post():
    if request.method == "POST":
        fncid = request.form['fncid']
        arg01 = request.form['arg01'] if 'arg01' in request.form else None
        arg02 = request.form['arg02'] if 'arg02' in request.form else None
        arg03 = request.form['arg03'] if 'arg03' in request.form else None

        if 'c' not in session:
            return "false"

        # Restore cookies
        s = requests.session()
        set_cookies(s, session['c'])

        query_content = function.ap_query(
            s, fncid, {"arg01": arg01, "arg02": arg02, "arg03": arg03})

        if fncid == "ag222":
            return json.dumps(parse.course(query_content))
        elif fncid == "ag008":
            return json.dumps(parse.score(query_content))

    return render_template("query.html")


@app.route('/leave', methods=["POST"])
@cross_origin(supports_credentials=True)
def leave_post():
    if request.method == "POST":
        arg01 = request.form['arg01'] if 'arg01' in request.form else None
        arg02 = request.form['arg02'] if 'arg02' in request.form else None


        # Restore cookies
        s = requests.session()
        set_cookies(s, session['c'])

        if arg01 and arg02:
            return json.dumps(function.leave_query(s, arg01, arg02))
        else:
            return json.dumps(function.leave_query(s))


@app.route('/leave/submit', methods=['POST'])
@cross_origin(supports_credentials=True)
def leave_submit():
    if request.method == 'POST':
        start_date = request.form['start_date'].replace("-", "/")
        end_date = request.form['end_date'].replace("-", "/")
        reason_id = request.form['reason_id'] if 'reason_id' in request.form else None
        reason_text = request.form['reason_text'] if 'reason_text' in request.form else None
        section = json.loads(request.form['section']) if 'section' in request.form else None

        s = requests.session()
        set_cookies(s, session['c'])

        start_date = start_date.split("/")
        start_date[0] = str(int(start_date[0]) - 1911)
        start_date = "/".join(start_date)

        end_date = end_date.split("/")
        end_date[0] = str(int(end_date[0]) - 1911)
        end_date = "/".join(end_date)


        if reason_id and reason_text and section:
            return json.dumps(function.leave_submit(s, start_date, end_date, reason_id, reason_text, section))
        else:
            return json.dumps((False, "Error..."))




@app.route('/bus/query', methods=["POST"])
@cross_origin(supports_credentials=True)
def bus_query():
    if request.method == "POST":
        date = request.form['date']


        # Restore cookies
        s = requests.session()
        set_cookies(s, session['c'])


        return json.dumps(function.bus_query(s, date))


@app.route('/bus/booking', methods=["POST"])
@cross_origin(supports_credentials=True)
def bus_booking():
    if request.method == "POST":
        busId = request.form['busId']
        action = request.form['action']


        # Restore cookies
        s = requests.session()
        set_cookies(s, session['c'])

        return json.dumps(function.bus_booking(s, busId, action))


@app.route('/notification/<page>')
@cross_origin(supports_credentials=True)
def notification(page):
    page = int(page)
    return json.dumps(function.notification_query(page))
 

if __name__ == '__main__':
    app.run(host="0.0.0.0")
