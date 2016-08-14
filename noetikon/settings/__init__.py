# -*- coding: utf8 -*-
import sys

from noetikon.settings.base import *  # noqa: F403
from noetikon.settings.noetikon import *  # noqa: F403
from noetikon.settings.rest_framework import *  # noqa: F403

try:
    from noetikon.settings.local import *  # noqa: F403
except ImportError:
    raise ImportError("Couldn't load local settings noetikon.settings.local")

if 'debug_toolbar' in INSTALLED_APPS:  # noqa: F405
    from noetikon.settings.debug_toolbar import *  # noqa: F403

if 'nopassword' in INSTALLED_APPS:  # noqa: F405
    from noetikon.settings.nopassword import *  # noqa: F403

if 'test' in sys.argv:
    from noetikon.settings.test import *  # noqa: F403

TEMPLATE_DEBUG = DEBUG  # noqa: F405
THUMBNAIL_DEBUG = DEBUG  # noqa: F405
