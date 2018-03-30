import os

from concertiaroma3.settings.base import *  # noqa

INSTANCE = 'alpha'

ALLOWED_HOSTS = [
    INSTANCE + '.concertiaroma.com'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'concertiaroma3_' + INSTANCE,
        'USER': 'concertiaroma3',
        'PASSWORD': os.environ.get('DATABASES_DEFAULT_PASSWORD', ''),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CONN_MAX_AGE = None

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True  # noqa

# Site

SITE_ID = 3

# ASSETS

STATIC_DEBUG = True
