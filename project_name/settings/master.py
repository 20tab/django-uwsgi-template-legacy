from {{ project_name }}.settings.base import *

ALLOWED_HOSTS = ('{{ project_name }}.com',)

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Add 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '{{ project_name }}',  # '/path/example.db'. Path to database file if using sqlite3.
        'USER': 'user',  # Not used with sqlite3.
        'PASSWORD': 'password',  # Not used with sqlite3.
        'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',  # Set to empty string for default. Not used with sqlite3.
    }
}

# Fab commands configuration
WORKING_DIR = "www/{{project_name}}"
HOST_USER = "30248"
HOST_IP = ""
HOST_PORT = "22"
