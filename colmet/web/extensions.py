# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.assets import Environment


cache = Cache()
assets = Environment()


def configure_extensions(app):
    cache.init_app(app)
    assets.init_app(app)

    if app.debug:
        DebugToolbarExtension(app)
