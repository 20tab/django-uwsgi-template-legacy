from {{ project_name }}.settings.base import *  # noqa

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ project_name }}',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Email

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# ASSETS

# STATIC_DEBUG = True

# Behave

# INSTALLED_APPS += ('behave_django',)

# BDD_DEFAULT_BROWSER = 'chrome'
# BDD_HEADLESS_BROWSER = True
# BDD_BROWSER_LANGUAGE = 'it-IT'
# BDD_DEFAULT_WAIT_TIME = 2

