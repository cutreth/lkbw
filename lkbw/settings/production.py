from .base import *

DEBUG = False

with open('/home/lkbw/private/DjangoKey.txt') as key:
    SECRET_KEY = key.read().strip()

with open('/home/lkbw/private/GoogleKey.txt') as key:
    WAGTAIL_ADDRESS_MAP_KEY = key.read().strip()
    GOOGLE_MAPS_V3_APIKEY = WAGTAIL_ADDRESS_MAP_KEY

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
