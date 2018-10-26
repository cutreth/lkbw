from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

with open("D:\KY\OneDrive\Documents\KY's Documents\GitHub\DjangoKey.txt") as key:
    SECRET_KEY = key.read().strip()

with open("D:\KY\OneDrive\Documents\KY's Documents\GitHub\GoogleKey.txt") as key:
    WAGTAIL_ADDRESS_MAP_KEY = key.read().strip()
    GOOGLE_MAPS_V3_APIKEY = WAGTAIL_ADDRESS_MAP_KEY

AWS_CLOUDFRONT_URL = ''  # Need this defined explicitly as null in dev to support "if" statement in block_tags

# Wagtail search settings

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.db',
    }
}

try:
    from .local import *
except ImportError:
    pass
