import os

from {{project_name}}.settings.base import *  # noqa
from {{project_name}}.settings.secret import *  # noqa

ALLOWED_HOSTS = (f'alpha.{BASE_HOST_URL}',)

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASES_DEFAULT_NAME or '{{project_name}}_alpha',
        'USER': DATABASES_DEFAULT_USER or '{{project_name}}',
        'PASSWORD': DATABASES_DEFAULT_PASSWORD or '',
        'HOST': DATABASES_DEFAULT_HOST or '127.0.0.1',
        'PORT': DATABASES_DEFAULT_PORT or '5432',
    }
}


# Email Settings
# https://docs.djangoproject.com/en/2.0/topics/email/

EMAIL_HOST = ''

# Sites
# https://docs.djangoproject.com/en/2.0/ref/contrib/sites/

# SITE_ID = 3

# ASSETS

# STATIC_DEBUG = True

# Fab commands configuration

WORKING_DIR = "www/{{project_name}}_alpha"
HOST_USER = ""
HOST_IP = ""
HOST_PORT = "22"
