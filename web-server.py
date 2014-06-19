# -*- coding: utf-8 -*-
import function
from flask import Flask, render_template, jsonify
from flask import request


app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/ap/login', methods=['POST'])
def login_post():
    account = request.form['account']
    password = request.form['password']

    if account=="" and password=="" :
    	return render_template('login.html')
    else:
    	return function.login(account,password)


@app.route('/ap/query', methods=['GET', 'POST'])
def query_post():
    #password = request.form['password']
    #ag_id = request.form['ag_id']

    #print(account, password)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        ag_id = request.form['ag_id']


        


    return render_template("query.html")



if __name__ == '__main__':
    app.run(debug=True)
