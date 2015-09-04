# -*- coding: utf-8 -*-

from flask import Blueprint
from flask.ext.autodoc import Autodoc

doc = Blueprint("doc", __name__, url_prefix="/v2/doc")
auto = Autodoc()


@doc.route('/')
@doc.route('/public')
def public_doc():
    return auto.html(title="KUAS API Documentation")
