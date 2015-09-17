# -*- coding: utf-8 -*-

import os
import json
import redis
import requests
from flask import g, abort
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


import kuas_api.kuas.cache as cache
import kuas_api.modules.const as const
import kuas_api.modules.error as error

# Create HTTP auth
auth = HTTPBasicAuth()

# Redis connection
red = redis.StrictRedis(db=2)

# Shit lazy key
DIRTY_SECRET_KEY = red.get("SECRET_KEY") if red.exists(
    "SECRET_KEY") else str(os.urandom(32))


def check_cookies(username):
    """Check username is exist in redis
    :param username: school id
    :type username: str
    :return: Exist then return  True, else return False
    :rtype: bool
    """
    return red.exists(username)


def set_cookies(s, username):
    """Reset cookies to requests.Session
    :param s: Requests session
    :type s: requests.sessions.Session
    :param username: school id
    :type username: str
    :return: None
    """
    cookies = json.loads(str(red.get(username), "utf-8"))

    for c in cookies:
        s.cookies.set(c['name'], c['value'], domain=c['domain'])


def get_requests_session_with_cookies():
    s = requests.Session()

    if g.username:
        set_cookies(s, g.username)

    return s


def generate_auth_token(username, cookies, expiration=600):
    """Generate auth token and save cookies to redis by username
    :param username: usrename (school id)
    :type username: str
    :param cookies: cookies list from :class:`requests.Session.cookies`
    :type cookies: :class:`requests.cookies.RequestsCookieJar`
    :return: auth token
    :rtype: str
    """
    s = Serializer(DIRTY_SECRET_KEY, expires_in=expiration)

    red.set(username, json.dumps(cookies))

    return s.dumps({"sid": username})


def verify_auth_token(token):
    """Verify auth token
    :param token: auth token from user
    :type token: str
    :return: None or username
    :rtype: str or None
    """
    s = Serializer(DIRTY_SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        abort(401)     # valid token, but expired
    except BadSignature:
        return None    # invalid token

    if not check_cookies(data['sid']):
        return None    # Cookies not exist in redis

    user = data['sid']
    return user


@auth.verify_password
def verify_password(username_or_token, password):
    """For verify username or token is valid.
    :param username_or_token: username or token
    :type username_or_token: str
    :param password: password for username, if using token,
    password can be ignore
    :type password: str
    :return: is the username and password, or token is valid
    :rtype: bool
    """
    # Check auth token
    username = verify_auth_token(username_or_token)

    # Set username and token to global
    if username:
        g.username = username
        g.token = username_or_token
    else:
        # If auth token is bad (valid token but expired, or invalid token)
        # Then Try to login to school service
        cookies = cache.login(username_or_token, password)

        # If cookies is False, mean login error
        # return False for unverify password
        if not cookies:
            return False

        # If return cookies list,
        # generate auth token and save cookies to redis
        # and set to g.token pass to /api_version/token
        # for return token.
        #
        # Data set in redis server:
        #   key: username, value: cookies
        g.token = generate_auth_token(
            username_or_token, cookies, expiration=const.token_duration)
        g.username = username_or_token

    return True


@auth.error_handler
def auth_error():
    """Return Authroized Error to users.

    :return: error json
    :rtype: json
    """

    user_message = ("Your token has been expired or "
                    "using wrong username and password to login")

    return error.error_handle(
        status=401,
        developer_message="Token expired or Unauthorized Access",
        user_message=user_message
    )
