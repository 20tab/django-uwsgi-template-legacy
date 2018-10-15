from {{project_name}}.settings.base import *  # noqa
from {{project_name}}.settings.secret import *  # noqa

HOST = BASE_HOST_URL
ALLOWED_HOSTS = (HOST,)

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASES_DEFAULT_NAME or '{{project_name}}_test',
        'USER': DATABASES_DEFAULT_USER or '{{project_name}}',
        'PASSWORD': DATABASES_DEFAULT_PASSWORD or '',
        'HOST': DATABASES_DEFAULT_HOST or '127.0.0.1',
        'PORT': DATABASES_DEFAULT_PORT or '5432',
    }
}

# Email Settings
# https://docs.djangoproject.com/en/2.1/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Debug

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa

# Assets

# STATIC_DEBUG = False

# Behave

INSTALLED_APPS += ('behave_django',)

# BDD_DEFAULT_BROWSER = 'chrome'
# BDD_HEADLESS_BROWSER = False
# BDD_INCOGNITO_BROWSER = True
# BDD_FULLSCREEN_BROWSER = False
# BDD_BROWSER_LANGUAGE = 'it-IT'
# BDD_DEFAULT_WAIT_TIME = 2
