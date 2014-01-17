# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from abc import ABCMeta
from flask import render_template
from werkzeug import exceptions


class KHTTPException(exceptions.HTTPException):
    '''Abstract K exception with common data.'''
    __metaclass__ = ABCMeta

    def get_headers(self, environ):
        '''Get a list of headers.'''
        return [('Content-Type', 'text/html; charset=UTF-8')]

    def get_body(self, environ):
        '''Get the body displayed when the exception is raised.'''
        return render_template('exception.html.jinja2',
                               message=self.message, code=self.code)


class BadRequest(KHTTPException):
    '''HTTP Error 400.'''
    code = 400
    message = \
        'Il y a eu un problème lors de la demande d’affichage de cette page.'


class Unauthorized(KHTTPException):
    '''HTTP Error 401.'''
    code = 401
    message = 'Vous devez être connecté pour accéder à cette page.'


class Forbidden(KHTTPException):
    '''HTTP Error 403.'''
    code = 403
    common = ""
    message = 'Vous n’êtes pas autorisé à accéder à cette page.'


class NotFound(KHTTPException):
    '''HTTP Error 404.'''
    code = 404
    message = 'Cette page n’existe pas.'


class MethodNotAllowed(KHTTPException):
    '''HTTP Error 405.'''
    code = 405
    message = \
        'La méthode utilisée pour accéder à cette page n’est pas autorisée.'


class NotAcceptable(KHTTPException):
    '''HTTP Error 406.'''
    code = 406
    message = 'Aucune réponse possible.'


class InternalServerError(KHTTPException):
    '''HTTP Error 500.'''
    code = 500
    message = 'Un problème est survenu durant l’affichage de cette page.'


def configure_errorhandlers(app):
    '''Register all the available errors in the `app`.'''
    if app.debug or app.testing:
        @app.errorhandler(400)
        def handle_bad_request_in_debug(exception):
            '''Add a request handler to debug 400 'Bad Request' exceptions.'''
            raise
    app.register_error_handler(400, BadRequest)
    app.register_error_handler(401, Unauthorized)
    app.register_error_handler(403, Forbidden)
    app.register_error_handler(404, NotFound)
    app.register_error_handler(405, MethodNotAllowed)
    app.register_error_handler(406, NotAcceptable)
    app.register_error_handler(500, InternalServerError)
