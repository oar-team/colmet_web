#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals
import pprint
import os
from flask import current_app
from flask.ext.script import Manager
from flask_script import Server
from flask.ext.script.commands import ShowUrls, Clean

from werkzeug.contrib.fixers import ProxyFix
from gevent.wsgi import WSGIServer

from colmet.web.app import create_app
from colmet.web.extensions import cache


def create_app_wrapper(config=None):
    if config is None:
        return create_app()
    here = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(here, config)
    return create_app(config_file)


class ServerCommand(Server):
    def handle(self, app, host, port, use_debugger, use_reloader,
               threaded, processes, passthrough_errors):
        host = app.config.get('HOST', host)
        port = app.config.get('PORT', port)
        if use_debugger:
            app.run(host=host,
                    port=port,
                    debug=use_debugger,
                    use_debugger=use_debugger,
                    use_reloader=use_reloader,
                    threaded=threaded,
                    processes=processes,
                    passthrough_errors=passthrough_errors,
                    **self.server_options)
        else:
            address = (host, port)
            app.wsgi_app = ProxyFix(app.wsgi_app)
            server = WSGIServer((host, port), app)
            try:
                print("Server running on port %s:%d. Ctrl+C to quit" % address)
                server.serve_forever()
            except KeyboardInterrupt:
                server.stop()
        print("\n")


manager = Manager(create_app_wrapper)
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())
manager.add_command("runserver", ServerCommand())


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


if __name__ == "__main__":
    manager.run()
