from {{project_name}}.settings.base import *  # noqa
from {{project_name}}.settings.secret import *  # noqa

HOST = f'beta.{BASE_HOST_URL}'
ALLOWED_HOSTS = (HOST,)


# Database
# https://docs.djangoproject.com/en/{{docs_version}}/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASES_DEFAULT_NAME or '{{project_name}}_beta',
        'USER': DATABASES_DEFAULT_USER or '{{project_name}}',
        'PASSWORD': DATABASES_DEFAULT_PASSWORD or '',
        'HOST': DATABASES_DEFAULT_HOST or '127.0.0.1',
        'PORT': DATABASES_DEFAULT_PORT or '5432',
    }
}


# Email Settings
# https://docs.djangoproject.com/en/{{docs_version}}/topics/email/

EMAIL_HOST = ''


# Debug

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa


# Assets

# STATIC_DEBUG = True


# Sites
# https://docs.djangoproject.com/en/{{docs_version}}/ref/contrib/sites/

# SITE_ID = 2


# Invoke commands configuration

WORKING_DIR = 'www/{{project_name}}_beta'
HOST_USER = ''
HOST_IP = ''
HOST_PORT = '22'
