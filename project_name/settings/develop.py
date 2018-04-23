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
        'NAME': os.environ.get('DATABASES_DEFAULT_NAME', '{{ project_name }}_dev'),
        'USER': os.environ.get('DATABASES_DEFAULT_USER', '{{ project_name }}'),
        'PASSWORD': os.environ.get('DATABASES_DEFAULT_PASSWORD', ''),
        'HOST': os.environ.get('DATABASES_DEFAULT_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DATABASES_DEFAULT_PORT', '5432',),
    }
}

# Email Settings
# https://docs.djangoproject.com/en/2.0/topics/email/

EMAIL_HOST = ''

# Sites
# https://docs.djangoproject.com/en/2.0/ref/contrib/sites/

# SITE_ID = 2

# ASSETS

# STATIC_DEBUG = True

# Fab commands configuration

WORKING_DIR = "www/{{project_name}}_dev"
HOST_USER = ""
HOST_IP = ""
HOST_PORT = "22"
