# -*- coding: utf-8 -*-
import function
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('finder.html')
@app.route('/ap/login', methods=['POST'])
def login_post():
    account = request.form['account']
    password = request.form['password']

    if account=="" and password=="" :
    	return render_template('login.html')
    else:
    	return function.login(account,password)
@app.route('/ap/curriculum', methods=['POST'])
def AG_post():
    account = request.form['account']
    password = request.form['password']
    AGID=request.form['AGID']

    if account=="" and password=="" :
    	return render_template('curriculum.html')
    else:
    	return function.curriculum(AGID,account,password)

if __name__ == '__main__':
    app.run(debug=True)
