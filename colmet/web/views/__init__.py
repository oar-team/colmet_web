# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from . import frontend


DEFAULT_BLUEPRINTS = (
    (frontend.frontend, ''),
)


def register_blueprints(app):
    for blueprint, url_prefix in DEFAULT_BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
