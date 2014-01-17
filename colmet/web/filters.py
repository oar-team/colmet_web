# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from werkzeug.urls import url_fix
from .utils.date import datetime_format, date_format
from .utils import domain, split, sort_by, slugify

__all__ = ['configure_template_filters']


def configure_template_filters(app):
    '''Declares all jinja2 filters for the application'''
    app.template_filter('datetime_format')(datetime_format)
    app.template_filter('date_format')(date_format)
    app.template_filter('domain')(domain)
    app.template_filter('split')(split)
    app.template_filter('sort_by')(sort_by)
    app.template_filter('slugify')(slugify)
    app.template_filter('url_fix')(url_fix)
