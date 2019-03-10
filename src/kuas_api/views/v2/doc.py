# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_autodoc.autodoc import Autodoc

doc = Blueprint("doc", __name__, url_prefix="/v2/docs")
auto = Autodoc()


@doc.route('/')
@doc.route('/public')
def public_doc():
    return auto.html(title="KUAS API Documentation")
