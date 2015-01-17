# -*- coding: utf8 -*-
from noetikon.settings.base import *
from noetikon.settings.noetikon import *
from noetikon.settings.rest_framework import *

try:
    from noetikon.settings.local import *
except ImportError as e:
    raise ImportError("Couldn't load local settings noetikon.settings.local")

if 'debug_toolbar' in INSTALLED_APPS:
    from noetikon.settings.debug_toolbar import *

if 'nopassword' in INSTALLED_APPS:
    from noetikon.settings.nopassword import *

TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True

