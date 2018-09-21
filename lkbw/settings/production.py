from .base import *

DEBUG = False

with open('/home/lkbw/lkbw/SecretKey.txt') as key:
	SECRET_KEY = key.read().strip()

ALLOWED_HOSTS = ['lkbw.pythonanywhere.com', 'www.lilkevbigworld.com'] 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lkbw$blog',
        'USER': 'lkbw',
        'PASSWORD': 'lkbwdbpw',
        'HOST': 'lkbw.mysql.pythonanywhere-services.com',
        'PORT': '',
    }
}

try:
    from .local import *
except ImportError:
    pass
