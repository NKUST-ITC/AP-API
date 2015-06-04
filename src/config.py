# -*- coding: utf-8 -*-

import os
from datetime import timedelta


DEBUG = True
SECRET_KEY = os.urandom(24)
SESSION_COOKIE_HTTPONLY = False
PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

CORS_ORIGINS = "http://localhost:8000"
