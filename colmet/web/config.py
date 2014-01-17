# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import os
import uuid


class DefaultConfig(object):
    '''Default configuration for the colmet web application.'''

    SESSION_COOKIE_NAME = 'colmet_auth'
    SECRET_KEY = "%s" % uuid.uuid4()
    SITE_DESCRIPTION = 'Visualizing the collected metrics about OAR jobs'
    SITE_TITLE = 'Colmet'

    # Locales
    LOCALE = 'fr_FR'
    TIZONE = 'Europe/Paris'

    # Server
    DEBUG = True
    TESTING = False
    HOST = '0.0.0.0'
    PORT = 9090

    # Cache
    CACHE_TYPE = 'null'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_KEY_PREFIX = 'colmet_web'
    CACHE_NO_NULL_WARNING = True

    # Acces point
    FILESYSTEM_PREFIX = os.path.join(os.path.dirname(__file__))
