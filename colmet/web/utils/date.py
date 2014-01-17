# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from flask import current_app
import arrow


def format_date(date, pattern, humanize):
    a = arrow.get(date).to('utc').to(current_app.config['TIMEZONE'])
    locale = current_app.config['LOCALE']
    if humanize:
        return a.humanize(locale)
    else:
        return a.format(pattern, locale)


def date_format(date, pattern="EEEE dd MMMM yyyy", humanize=False):
    """Date formatter"""
    if date is None:
        return ""
    return date.strftime('%d/%m/%Y')


def datetime_format(datetime, pattern="EEEE dd MMMM yyyy - HH'h'mm",
                    humanize=False):
    """Date (with time) formatter"""
    return format_date(datetime, pattern=pattern, humanize=humanize)
