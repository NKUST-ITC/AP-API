import json
from flask import request, jsonify
from flask_apiblueprint import APIBlueprint
from flask_cors import *

import kuas_api.kuas.ap as ap
import kuas_api.kuas.function as function

from kuas_api.views.v1 import api_v1
import kuas_api.modules.error as error
import kuas_api.modules.const as const


api_v2 = APIBlueprint(
    'api_v2', __name__,
    subdomain='',
    url_prefix='/v2')


@api_v2.route('/')
def version_2():
    """Return default version
    """
    return "kuas-api version 2"


@api_v2.route('/versions/<string:device_type>')
def device_version(device_type):
    if device_type in const.device_version:
        result = {
            "version": {
                "device": device_type,
                "version": const.device_version[device_type]
            }
        }

        return jsonify(result)

    return error.error_handle(status=400,
                              developer_message="Device not found.",
                              user_message="Device not found.")


@api_v2.route('/servers/status')
def servers_status():
    try:
        original_status = function.server_status()
    except Exception as err:
        return error.error_handle(status=400,
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


@api_v2.route('/ap/semester')
@cross_origin(supports_credentials=True)
def ap_semester():
    semester_list = ap.get_semester_list()
    default_yms = list(filter(lambda x: x['selected'] == 1, semester_list))[0]

    # Check default args
    if request.args.get("default") == "1":
        return json.dumps({"default_yms": default_yms}, ensure_ascii=False)

    # Check limit args
    limit = request.args.get("limit")
    if limit:
        try:
            semester_list = semester_list[: int(limit)]
        except ValueError:
            return error.error_handle(status=400,
                                      developer_message="Error value for limit.",
                                      user_message="To type a wrong value for limit.")

    return json.dumps({"semester": semester_list,
                       "default": default_yms}, ensure_ascii=False)
