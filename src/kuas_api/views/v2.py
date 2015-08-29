from flask import jsonify
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
    url_prefix='/v2',
    inherit_from=api_v1)


@api_v2.route('/')
def version_2():
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


@api_v1.route('/ap/semesters')
@cross_origin(supports_credentials=True)
def ap_semester():
    semester_list = ap.get_semester_list()
    default_yms = list(filter(lambda x: x['selected'] == 1, semester_list))[0]
    
    return json.dumps({"semester": semester_list,
                       "default_yms": default_yms}, ensure_ascii=False)
