# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
import logging
from .utils.color_formatter import make_colored_stream_handler


def configure_logging(app):
    if app.testing:
        return

    app.logger.handlers = []
    handlers = []
    handler = make_colored_stream_handler()
    handlers.append(handler)

    if not app.debug:
        app.logger.setLevel(logging.ERROR)
    logging.getLogger('flask').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.INFO)

    for handler in handlers:
        app.logger.addHandler(handler)
        logging.getLogger('flask').addHandler(handler)
        logging.getLogger('werkzeug').addHandler(handler)
