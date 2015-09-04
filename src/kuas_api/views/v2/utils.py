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
    """RESTful stateless login
    Using HTTP Basic Authonication

    curl -u guest:123 -i -X GET http://localhost:5001/v2/token
    """
    token = g.token
    return jsonify({
        'token': token.decode('ascii'),
        'duration': const.token_duration
    })


@route('/versions/<string:device_type>')
@auto.doc(groups=["public"])
def device_version(device_type):
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
