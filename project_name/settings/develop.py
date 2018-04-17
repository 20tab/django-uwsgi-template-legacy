import os

from {{project_name}}.settings.base import *  # noqa

ALLOWED_HOSTS = (f'dev.{BASE_HOST_URL}',)

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ project_name }}_dev',
        'USER': '{{ project_name }}',
        'PASSWORD': os.environ.get('DATABASES_DEFAULT_PASSWORD', ''),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Email

EMAIL_HOST = ''

# Site

# SITE_ID = 2

# ASSETS

# STATIC_DEBUG = True

# Fab commands configuration

WORKING_DIR = "www/{{project_name}}_dev"
HOST_USER = ""
HOST_IP = ""
HOST_PORT = "22"
