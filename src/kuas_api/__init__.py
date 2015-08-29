# -*- coding: utf-8 -*-

import os
import json
from functools import wraps

import requests
import kuas_api.kuas.ap as ap
import kuas_api.kuas.user as user
import kuas_api.kuas.function as function

from flask import Flask, render_template, request, session
from flask_cors import *

__version__ = "2.0"

android_version = "1.5.4"
android_donate_version = "2.0.0"
ios_version = "1.4.3"

app = Flask(__name__)
app.config.from_object("config")

from kuas_api.views.v1 import api_v1
app.register_blueprint(api_v1)

from kuas_api.views.v2 import api_v2
app.register_blueprint(api_v2)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
