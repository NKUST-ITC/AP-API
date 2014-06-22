# -*- coding: utf-8 -*-

import json
import uniout
import parse
import function
from flask import Flask, render_template, request, \
    session
from flask_cors import *

app = Flask(__name__)
app.config['SESSION_COOKIE_HTTPONLY'] = False


origins = "http://localhost:8000"
#origins = "*"


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/ap/login', methods=['POST'])
@cross_origin(supports_credentials=True, origins=origins)
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
@cross_origin(supports_credentials=True, origins=origins)
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
@cross_origin(supports_credentials=True, origins=origins)
def query_post():
    if request.method == "POST":
        username = request.form['username'] if 'username' in request.form else None
        password = request.form['password'] if 'password' in request.form else None
        fncid = request.form['fncid']

        if 's' not in session:
            return "you did't login"

        if not function.is_login(session['s']):
            return "false"

        query_content = function.query(session['s'], username, password, fncid)
        #open("c.html", "w").write(json.dumps(parse.course(query_content)))
        return json.dumps(parse.course(query_content))

    return render_template("query.html")


if __name__ == '__main__':
    app.secret_key = "testing"
    app.run(host="0.0.0.0", debug=True)
