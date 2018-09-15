"""
WSGI config for lkbw project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

if sys.platform == 'win32':
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lkbw.settings.dev")

else:
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lkbw.settings.production")

application = get_wsgi_application()
