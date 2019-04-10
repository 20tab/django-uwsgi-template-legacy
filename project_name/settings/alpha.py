"""Django settings for alpha environment."""

from {{project_name}}.settings.base import *  # noqa
from {{project_name}}.settings.secret import *  # noqa

HOST = f'alpha.{BASE_HOST_URL}'  # noqa

ALLOWED_HOSTS = (HOST,)


# Database
# https://docs.djangoproject.com/en/{{docs_version}}/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASES_DEFAULT_NAME or '{{project_name}}_alpha',  # noqa
        'USER': DATABASES_DEFAULT_USER or '{{project_name}}',  # noqa
        'PASSWORD': DATABASES_DEFAULT_PASSWORD or '',  # noqa
        'HOST': DATABASES_DEFAULT_HOST or '127.0.0.1',  # noqa
        'PORT': DATABASES_DEFAULT_PORT or '5432',  # noqa
    }
}


# Email Settings
# https://docs.djangoproject.com/en/{{docs_version}}/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = EMAIL_HOST or ''  # noqa


# Debug

DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa
