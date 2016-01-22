from {{ project_name }}.settings.base import *

ALLOWED_HOSTS = ('dev.{{ project_name }}.com',)

DEBUG = True
TEMPLATES[0]['DEBUG'] = True

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