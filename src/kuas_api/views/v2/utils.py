# -*- coding: utf-8 -*-
from flask import g, jsonify

import kuas_api.kuas.cache as cache
import kuas_api.modules.error as error
import kuas_api.modules.const as const
from kuas_api.modules.stateless_auth import auth
from .doc import auto

# Nestable blueprints problem
# not sure isn't this a best practice now.
# https://github.com/mitsuhiko/flask/issues/593
#from kuas_api.views.v2 import api_v2
routes = []


def route(rule, **options):
    def decorator(f):
        url_rule = {
            "rule": rule,
            "view_func": f,
            "options": options if options else {}
        }

        routes.append(url_rule)
        return f

    return decorator


@route("/token")
@auto.doc(groups=["public"])
@auth.login_required
def get_auth_token():
    """Login to KUAS, and return token for KUAS API.

    **Example request**:

    .. sourcecode:: http

        GET /latest/token HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=
        Accept: */*

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "duration": 600,
          "token_type": "Basic",
          "auth_token": "adfakdflakds.fladkjflakjdf.adslkfakdadf"
        }


    :statuscode 200: success login
    :statuscode 401: login fail or auth_token expired
    """

    token = g.token
    return jsonify(
        auth_token=token.decode('ascii'),
        token_type="Basic",
        duration=const.token_duration)


@route('/versions/<string:device_type>')
@auto.doc(groups=["public"])
def device_version(device_type):
    """Get latest version for app on (`device_type`) in webstore.

    **Example request**

    .. sourcecode:: http

            GET /latest/versions/android HTTP/1.1
            Host: kuas.grd.idv.tw:14769



    **Response**

    +----------------+---------------+-------------------------------------------+
    |                |               |                                           |
    | Parameter Name | Type          | Description                               |
    |                |               |                                           |
    +================+===============+===========================================+
    |                |               |                                           |
    | version        | Object        |                                           |
    |                |               |                                           |
    +----------------+---------------+-------------------------------------------+

    **Version object**

    +----------------+---------------+-------------------------------------------+
    |                |               |                                           |
    | Parameter Name | Type          | Description                               |
    |                |               |                                           |
    +================+===============+===========================================+
    |                |               |                                           |
    | device         | String        | The device you request                    |
    |                |               |                                           |
    +----------------+---------------+-------------------------------------------+
    |                |               |                                           |
    | version        | String        | Latest version for device                 |
    |                |               |                                           |
    +----------------+---------------+-------------------------------------------+

    **Example response**

    .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
              "version": {
                "device": "android",
                "version": "1.5.4"
              }
            }



    """

    if device_type in const.device_version:
        result = {
            "version": {
                "device": device_type,
                "version": const.device_version[device_type]
            }
        }

        return jsonify(result)

    return error.error_handle(status=404,
                              developer_message="Device not found.",
                              user_message="Device not found.")


@route('/servers/status')
@auto.doc(groups=["public"])
def servers_status():
    try:
        original_status = cache.server_status()
    except Exception as err:
        return error.error_handle(status=404,
                                  developer_message=str(err),
                                  user_message="Something wrong.")

    status = {
        "status": [
            {"service": "ap", "status": original_status[0]},
            {"service": "bus", "status": original_status[1]},
            {"service": "leave", "status": original_status[2]}
        ]
    }

    return jsonify(status)
