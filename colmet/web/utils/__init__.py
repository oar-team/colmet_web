# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import os
import re
import urlparse
import unidecode
# from werkzeug.utils import cached_property


def touch(fname, times=None):
    dirname = '/'.join(fname.split('/')[:-1])
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with file(fname, 'a'):
        os.utime(fname, times)


def domain(url):
    '''
    Returns the domain of a URL e.g. http://reddit.com/ > reddit.com
    '''
    rv = urlparse.urlparse(url).netloc
    if rv.startswith("www."):
        rv = rv[4:]
    return rv


def slugify(string):
    ''' Remove special char in string '''
    string = unidecode.unidecode(string).lower()
    return re.sub(r'\W+', '-', string).strip('-')


def sort_by(value, key=None, reverse=False, case_sensitive=True, attr=True):
    '''Sort an iterable ``value`` by ``key``.'''
    if key:
        if not attr:
            if case_sensitive:
                sort_func = lambda item: item[key]
            else:
                sort_func = lambda item: item[key].lower()
        else:
            if case_sensitive:
                sort_func = lambda item: item.__dict__[key]
            else:
                sort_func = lambda item: item.__dict__[key].lower()
    else:
        sort_func = None
    return sorted(value, key=sort_func, reverse=reverse)


def split(value, key='\n'):
    '''Sort an iterable ``value`` by ``key``.'''
    return value.split(key)
