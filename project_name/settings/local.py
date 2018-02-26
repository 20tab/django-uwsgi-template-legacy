from {{ project_name }}.settings.base import *  # noqa

ALLOWED_HOSTS = ('localhost', '127.0.0.1', '{{ project_name }}.local)

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

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'

# Debug

DEBUG = True
if DEBUG:
    TEMPLATES[0]['OPTIONS']['debug'] = True  # noqa

try:
    import debug_toolbar
except ModuleNotFoundError:
    pass
else:
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    INSTALLED_APPS.append('debug_toolbar')  # noqa
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': {
            'debug_toolbar.panels.redirects.RedirectsPanel',
            'debug_toolbar.panels.templates.TemplatesPanel'
        },
    }

# ASSETS

STATIC_DEBUG = True

# uWSGI

UWSGI_ACCESS_LOG_BASE_PATH = f'{BASE_DIR}/{{ project_name }}_access-'

