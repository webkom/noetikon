# -*- coding: utf8 -*-
import sys

from noetikon.settings.base import *  # noqa
from noetikon.settings.noetikon import *  # noqa
from noetikon.settings.rest_framework import *  # noqa

try:
    from noetikon.settings.local import *  # noqa
except ImportError:
    raise ImportError("Couldn't load local settings noetikon.settings.local")

if 'debug_toolbar' in INSTALLED_APPS:
    from noetikon.settings.debug_toolbar import *  # noqa

if 'nopassword' in INSTALLED_APPS:
    from noetikon.settings.nopassword import *  # noqa

if 'test' in sys.argv:
    from noetikon.settings.test import *  # noqa

TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
