from .base import *

from elasticsearch import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

DEBUG = False

with open('/home/lkbw/private/DjangoKey.txt') as key:
    SECRET_KEY = key.read().strip()

with open('/home/lkbw/private/GoogleKey.txt') as key:
    WAGTAIL_ADDRESS_MAP_KEY = key.read().strip()
    GOOGLE_MAPS_V3_APIKEY = WAGTAIL_ADDRESS_MAP_KEY

# Wagtail search settings

with open('/home/lkbw/private/AwsAccessKey.txt') as key:
    AWS_ACCESS_KEY = key.read().strip()

with open('/home/lkbw/private/AwsSecretKey.txt') as key:
    AWS_SECRET_KEY = key.read().strip()

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.elasticsearch6',
        'INDEX': 'wagtail',
        'TIMEOUT': 5,
        'HOSTS': [{
            'host': 'search-lkbw-o36dz33nhninyp4zptohj24ezq.us-east-2.es.amazonaws.com',
            'port': 443,
            'use_ssl': True,
            'verify_certs': True,
            'http_auth': AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, 'us-east-2', 'es'),
        }],
        'OPTIONS': {
            'connection_class': RequestsHttpConnection,
        },
    }
}

# PRD infastructure settings

ALLOWED_HOSTS = ['www.lilkevbigworld.com'] 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lkbw$blog',
        'USER': 'lkbw',
        'PASSWORD': 'lkbwdbpw',
        'HOST': 'lkbw.mysql.pythonanywhere-services.com',
        'PORT': '',    
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

try:
    from .local import *
except ImportError:
    pass
