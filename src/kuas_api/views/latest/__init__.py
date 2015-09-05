# -*- coding: utf-8 -*-

from flask_apiblueprint import APIBlueprint
from kuas_api.views.v2 import api_v2

# Create latest blueprint
latest = APIBlueprint(
    'latest', __name__,
    subdomain='',
    url_prefix='/latest',
    inherit_from=api_v2)
