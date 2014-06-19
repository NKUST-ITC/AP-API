# -*- coding: utf-8 -*-
import function
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/ap/login', methods=['POST'])
def login_post():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        is_login = function.login(username, password)

        if is_login:
            return "login"
        else:
            return "fail"


    return render_template("login.html")


@app.route('/ap/query', methods=['GET', 'POST'])
def query_post():
    if request.method == "POST":
        username = request.form['username'] if 'username' in request.form else None
        password = request.form['password'] if 'password' in request.form else None
        fncid = request.form['fncid']


        query_content = function.query(username, password, fncid)
        return query_content

    return render_template("query.html")


if __name__ == '__main__':
    app.run(debug=True)
