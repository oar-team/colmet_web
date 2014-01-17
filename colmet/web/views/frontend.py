# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from flask import Blueprint
from ..extensions import cache

frontend = Blueprint('frontend', __name__)


@frontend.route('/')
@cache.cached()
def index(page=1):
    return "Hello"
