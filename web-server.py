# -*- coding: utf-8 -*-

import json
import uniout
import parse
import function
from flask import Flask, render_template, request, session
from flask_cors import *

__version__ = "1.2.3 testing for memcached session"

android_version = "1.2.3"
ios_version = "1.1.0"


app = Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.secret_key = "This is Secret Key"


origins = "http://localhost:8000"
app.config["CORS_ORIGINS"] = origins


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

@app.route('/ios_version')
@cross_origin(supports_credentials=True)
def i_version():
    return ios_version


@app.route('/ap/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login_post():
    print(request.method)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']


        hash_value = function.login(username, password)

        if hash_value:
            session['s'] = hash_value
            return "true"
        else:
            return "false"


    return render_template("login.html")

@app.route('/ap/is_login', methods=['POST'])
@cross_origin(supports_credentials=True)
def is_login():
    if 's' not in session:
        print("no session")
        return "false"

    if function.is_login(session['s']):
        print("login success")
        return "true"
    else:
        print("login unsuccess")
        return "false"


@app.route('/ap/query', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def query_post():
    if request.method == "POST":
        username = request.form['username'] if 'username' in request.form else None
        password = request.form['password'] if 'password' in request.form else None
        fncid = request.form['fncid']
        arg01 = request.form['arg01'] if 'arg01' in request.form else None
        arg02 = request.form['arg02'] if 'arg02' in request.form else None
        arg03 = request.form['arg03'] if 'arg03' in request.form else None

        if 's' not in session:
            return "you did't login"

        if not function.is_login(session['s']):
            return "false"

        query_content = function.query(
            session['s'], username, password, 
            fncid, {"arg01": arg01, "arg02": arg02, "arg03": arg03})
        #open("c.html", "w").write(json.dumps(parse.course(query_content)))
        

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

        if arg01 and arg02:
            return json.dumps(function.leave_query(session['s'], arg01, arg02))
        else:
            return json.dumps(function.leave_query(session['s']))


@app.route('/bus/query', methods=["POST"])
@cross_origin(supports_credentials=True)
def bus_query():
    if request.method == "POST":
        date = request.form['date']
        print(date)
        return json.dumps(function.bus_query(session['s'], date))

@app.route('/bus/booking', methods=["POST"])
@cross_origin(supports_credentials=True)
def bus_booking():
    if request.method == "POST":
        busId = request.form['busId']
        action = request.form['action']

        return json.dumps(function.bus_booking(session['s'], busId, action))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
