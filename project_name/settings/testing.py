from {{project_name}}.settings.base import *  # noqa

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASES_DEFAULT_NAME', '{{ project_name }}_test'),
        'USER': os.environ.get('DATABASES_DEFAULT_USER', 'user'),
        'PASSWORD': os.environ.get('DATABASES_DEFAULT_PASSWORD', 'password'),
        'HOST': os.environ.get('DATABASES_DEFAULT_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DATABASES_DEFAULT_PORT', '5432',),
    }
}


# Email Settings
# https://docs.djangoproject.com/en/2.0/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


# ASSETS

# STATIC_DEBUG = True


# Behave

# INSTALLED_APPS += ('behave_django',)

# BDD_DEFAULT_BROWSER = 'chrome'
# BDD_HEADLESS_BROWSER = False
# BDD_BROWSER_LANGUAGE = 'it-IT'
# BDD_DEFAULT_WAIT_TIME = 2
