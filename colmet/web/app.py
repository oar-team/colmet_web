# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from flask import Flask

from .context import configure_context_processors
from .exceptions import configure_errorhandlers
from .extensions import configure_extensions
from .filters import configure_template_filters
from .logger import configure_logging
from .views import register_blueprints
from .config import DefaultConfig


def create_app(config_file=None):
    app = Flask("colmet")
    app.jinja_env.trim_blocks = True
    app.config.from_object(DefaultConfig)
    app.config.from_envvar('COLMET_WEB_CONFIG', silent=True)
    if config_file is not None:
        app.config.from_pyfile(config_file, silent=True)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_template_filters(app)
    configure_context_processors(app)
    register_blueprints(app)
    configure_logging(app)
    return app
