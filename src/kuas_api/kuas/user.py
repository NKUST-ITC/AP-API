# -*- coding: utf-8 -*-

from flask import g
import kuas_api.kuas.ap as ap
import kuas_api.kuas.cache as cache
from lxml import etree

AP_QUERY_USER_EXPIRE = 300


def _get_user_info(session):
    """Get user info

    return: `lxml.etree._Element`
    """

    content = cache.ap_query(
        session, "ag003", {}, g.username, expire=AP_QUERY_USER_EXPIRE)

    root = etree.HTML(content)

    return root


def get_user_info(session):
    root = _get_user_info(session)
    td = root.xpath("//td")

    result = {
        "education_system": "",
        "department": "",
        "class": "",
        "student_id": "",
        "student_name_cht": "",
        "student_name_eng": ""
    }

    result["education_system"] = td[3].text[5:]
    result["department"] = td[4].text[5:]
    result["class"] = td[8].text[5:]
    result["student_id"] = td[9].text[5:]
    result["student_name_cht"] = td[10].text[5:]
    result["student_name_eng"] = td[11].text[5:]

    return result


def get_user_picture(session):
    root = _get_user_info(session)

    try:
        image = ap.AP_BASE_URL + "/kuas" + \
            root.xpath("//img")[0].values()[0][2:]
    except:
        image = ""

    return image
