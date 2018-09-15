from .base import *

DEBUG = False

with open('/home/lkbw/lkbw/SecretKey.txt') as key:
	SECRET_KEY = key.read().strip()

ALLOWED_HOSTS = ['lkbw.pythonanywhere.com'] 
	
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lkbw$default',
		'USER': 'lkbw',
		'PASSWORD': 'lkbwdbpw',
		'HOST': 'lkbw.mysql.pythonanywhere-services.com',
    }
}

try:
    from .local import *
except ImportError:
    pass
