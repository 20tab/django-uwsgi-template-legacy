from __future__ import unicode_literals
"""
Django settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


gettext = lambda s: s

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cookielaw',
]

MANAGERS = (("errors", "errors@mantainer-domain.com"),)
ADMINS = MANAGERS
SERVER_EMAIL = 'errors@mantainer-domain.com'

# !!! set EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j!7z%+(kog8tqv-%y7ga5a#0i+!mc_436p2u&i_v9uy1@!#^&t'


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


ROOT_URLCONF = '{{ project_name }}.urls'

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'it-it'

MODELTRANSLATION_DEFAULT_LANGUAGE = 'it'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.abspath('static')
MEDIA_ROOT = os.path.abspath('media')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
