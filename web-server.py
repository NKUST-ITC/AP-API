# -*- coding: utf-8 -*-

import function
from flask import Flask, render_template, request, jsonify, session
from flask_cors import *

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/ap/login', methods=['POST'])
@cross_origin()
def login_post():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        hash_value = function.login(username, password)

        if is_login:
            session['s'] = hash_value
            return "login"
        else:
            return "fail"


    return render_template("login.html")


@app.route('/ap/query', methods=['GET', 'POST'])
@cross_origin()
def query_post():
    if request.method == "POST":
        username = request.form['username'] if 'username' in request.form else None
        password = request.form['password'] if 'password' in request.form else None
        fncid = request.form['fncid']

        if 's' not in session:
            return "you did't login"

        query_content = function.query(session['s'], username, password, fncid)
        return query_content

    return render_template("query.html")


if __name__ == '__main__':
    app.secret_key = "testing"
    app.run(debug=True)


<!DOCTYPE html>
<html>
<head>
<script src="/jquery/jquery-1.11.1.min.js">
</script>
<script>
$(document).ready(function(){
  $("button").click(function(){
    $.post("http://api.grd.idv.tw:14768/ap/login",
    {
      username:"1102108133",
      password:"111"
    },
    function(data,status){
      alert("IN");
      alert("数据：" + data + "\n状态：" + status);
    });
  });
});
</script>
</head>
<body>

<button>向页面发送 HTTP POST</button>

</body>
</html>
