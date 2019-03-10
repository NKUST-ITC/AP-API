# -*- coding: utf-8 -*-
import os
DEBUG = True
SECRET_KEY = "sdfsdhpmrgewf"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
#PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

UNITTEST_USERNAME = os.environ.get('USERNAME', '')
UNITTEST_PASSWORD = os.environ.get('PASSWORD', '')
