# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import datetime


def configure_context_processors(app):
    @app.context_processor
    def inject_date():
        ''' Add context variable. '''
        return dict(now=datetime.datetime.now)

    @app.context_processor
    def get_config():
        return dict(config=app.config)
