#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
import pprint
import os
from werkzeug.contrib.fixers import ProxyFix
from gevent.wsgi import WSGIServer

from flask import current_app
from flask.ext.script import Manager
from flask.ext.script.commands import ShowUrls, Clean

from colmet.web.app import app, configure_app
from colmet.web.extensions import cache


def init_app_hadler(config=None):
    if config is not None:
        here = os.path.abspath(os.path.dirname(__file__))
        config = os.path.join(here, config)
    return configure_app(app, config)


manager = Manager(init_app_hadler)
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.command
def clear_cache():
    cache.cache.clear()


@manager.command
def dumpconfig():
    "Dumps config"
    pprint.pprint(current_app.config)


@manager.shell
def make_shell_context():
    return dict(app=current_app)


manager.add_option("-c", "--config",
                   dest="config",
                   help="config file",
                   required=False)


@manager.command
def runserver(bind=None, port=None, gevent=False):
    """Runs the Flask server with Gevent or Werkzeug (debugger). """
    if bind is not None:
        app.config['HOST'] = bind
    if port is not None:
        app.config['PORT'] = port
    if not (gevent or not app.debug):
        app.run(host=app.config['HOST'],
                port=app.config['PORT'],
                threaded=True)
    else:
        app.wsgi_app = ProxyFix(app.wsgi_app)
        address = app.config['HOST'], app.config['PORT']
        server = WSGIServer(address, app)
        try:
            print("Server running on port %s:%d. Ctrl+C to quit" % address)
            server.serve_forever()
        except KeyboardInterrupt:
            server.stop()


if __name__ == "__main__":
    manager.run()
