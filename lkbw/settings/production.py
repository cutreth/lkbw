from .base import *

DEBUG = False

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
