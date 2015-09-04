# -*- coding: utf-8 -*-
import json


def error_handle(status,
                 developer_message, user_message,
                 error_code=-1, more_info=""):
    """Return error handler json
    :param status: HTTP status code
    :type status: int
    :param developer_message: message for developer
    :type developer_message: str
    :param user_message: message for user
    :type user_message: str
    :param error_code: internal error code
    :type error_code: int
    :param more_info: links for more information
    :type more_info: str

    :return: json error handle
    :rtype: json
    """

    error_handle = {
        "status": status,
        "developer_message": developer_message,
        "user_message": user_message,
        "error_code": error_code,
        "more_info": more_info
    }

    return json.dumps(error_handle)
