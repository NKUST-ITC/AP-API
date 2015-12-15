#-*- encoding=utf-8 -*-
"""This module `ap` provide manipulate of kuas AP system.
"""

__version__ = 2.0

import requests
from lxml import etree

# AP URL Setting
#: AP sytem base url
AP_BASE_URL = "http://140.127.113.224"

#: AP system login url
AP_LOGIN_URL = AP_BASE_URL + "/kuas/perchk.jsp"

#: AP system general query url, with two args,
#  first: prefix of qid, second: qid
AP_QUERY_URL = AP_BASE_URL + "/kuas/%s_pro/%s.jsp?"

#: AP guest account
AP_GUEST_ACCOUNT = "guest"

#: AP guest password
AP_GUEST_PASSWORD = "123"

# Timeout Setting
#: Login timeout
LOGIN_TIMEOUT = 1.0

#: Query timeout
QUERY_TIMEOUT = 5.0


def status():
    """Return AP server status code

    :rtype: int
    :returns: A HTTP status code

    >>> status()
    200
    """
    try:
        ap_status_code = requests.head(
            AP_BASE_URL,
            timeout=LOGIN_TIMEOUT).status_code
    except requests.exceptions.Timeout:
        ap_status_code = 408

    return ap_status_code


def login(session, username, password, timeout=LOGIN_TIMEOUT):
    """Login to KUAS AP system.

    :param session: requests session object
    :type session: class requests.sessions.Session
    :param username: username of kuas ap system, actually your kuas student id
    :type username: str or int
    :param password: password of kuas ap system.
    :type password: str or int
    :param timeout: login timeout
    :type timeout: int

    :return: login status
    :rtype: bool


    Login with correct username and password

    >>> s = requests.Session()
    >>> login(s, "guest", "123")
    True


    Login with bad username or password

    >>> login(s, "guest", "777")
    False
    """

    payload = {"uid": username, "pwd": password}

    # If timeout, return false
    try:
        r = session.post(AP_LOGIN_URL, data=payload, timeout=timeout)
    except requests.exceptions.Timeout:
        return False

    root = etree.HTML(r.text)

    try:
        is_login = not root.xpath("//script")[-1].text.startswith("alert")
    except:
        is_login = False

    return is_login


def get_semester_list():
    """Get semester list from ap system.

    :rtype: dict

    >>> get_semester_list()[-1]['value']
    '92,2'
    """

    s = requests.Session()
    login(s, AP_GUEST_ACCOUNT, AP_GUEST_PASSWORD)

    content = query(s, "ag304_01")
    root = etree.HTML(content)

    options = root.xpath("id('yms_yms')/option")
    options = map(lambda x: {"value": x.values()[0].replace("#", ","),
                             "selected": 1 if "selected" in x.values() else 0,
                             "text": x.text},
                  root.xpath("id('yms_yms')/option")
                  )
    options = list(options)

    return options


def query(session, qid, args={}):
    """Query AP system page by qid and args

    :param session: requests session object, the session must login first.
    :type session: class requests.sessions.Session
    :param qid: query id of ap system page
    :type qid: str
    :param args: arguments of query post
    :type args: dict

    :return" content of query page
    :rtype: str

    You must login first when using query
    Otherwise ap system won't let you use it.

    >>> s = requests.Session()
    >>> content = query(s, "ag222", {"arg01": "103", "arg02": "2"})
    >>> "Please Logon" in content
    True


    Login to guest

    >>> login(s, "guest", "123")
    True

    Query course data (ag202)

    >>> args = {"yms_yms": "103#2", "dgr_id": "14", "unt_id": "UC02", \
                "clyear": "", "sub_name": "", "teacher": "", "week": 2, \
                "period": 4, "reading": "reading"}
    >>> content = query(s, "ag202", args)
    >>> "內部控制暨稽核制度" in content
    True
    """

    data = {"arg01": "", "arg02": "", "arg03": "",
            "fncid": "", "uid": ""}

    data['fncid'] = qid

    for key in args:
        data[key] = args[key]

    try:
        resp = session.post(AP_QUERY_URL % (qid[:2], qid),
                            data=data,
                            timeout=QUERY_TIMEOUT
                            )
        resp.encoding = "utf-8"
        content = resp.text
    except requests.exceptions.ReadTimeout:
        content = ""

    return content


if __name__ == "__main__":
    import doctest
    doctest.testmod()
