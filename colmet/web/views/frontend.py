# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from flask import Blueprint, render_template
from ..extensions import cache

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@cache.cached()
def index():
    data = {"name": "colmet"}
    return render_template('/index.html.jinja2', **data)
