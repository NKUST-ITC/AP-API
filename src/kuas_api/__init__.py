# -*- coding: utf-8 -*-
from flask import Flask
from flask_sslify import SSLify

__version__ = "2.0"


app = Flask(__name__)
app.config.from_object("config")
sslify = SSLify(app)

from kuas_api.views.v1 import api_v1
app.register_blueprint(api_v1)

from kuas_api.views.v2 import api_v2
app.register_blueprint(api_v2)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
