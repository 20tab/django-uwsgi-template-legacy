from {{ project_name }}.settings.base import *


ALLOWED_HOSTS = ('localhost', '127.0.0.1')
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True
USE_DEBUG_TOOLBAR = True
INTERNAL_IPS = ('127.0.0.1', socket.gethostbyname(socket.gethostname()))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '{{ project_name }}',  # '/path/example.db'. Path to database file if using sqlite3.
        'USER': 'user',  # Not used with sqlite3.
        'PASSWORD': 'password',  # Not used with sqlite3.
        'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',  # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')
DEBUG_TOOLBAR_PATCH_SETTINGS = False
SHOW_TOOLBAR_CALLBACK = True

CLONEDIGGER_CONFIG = {
    'IGNORE_DIRS': ['fabfile.py', 'manage.py', '{{project_name}}','migrations',]
}