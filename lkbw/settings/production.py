from .base import *

DEBUG = False

with open('/home/lkbw/lkbw/SecretKey.txt') as key:
	SECRET_KEY = key.read().strip()

ALLOWED_HOSTS = ['lkbw.pythonanywhere.com', 'lilkevbigworld.com'] 

try:
    from .local import *
except ImportError:
    pass
