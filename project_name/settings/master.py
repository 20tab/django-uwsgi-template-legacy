from {{project_name}}.settings.base import *  # noqa

ALLOWED_HOSTS = (f'{BASE_HOST_URL}', f'www.{BASE_HOST_URL}')

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASES_DEFAULT_NAME', '{{ project_name }}'),
        'USER': os.environ.get('DATABASES_DEFAULT_USER', '{{ project_name }}'),
        'PASSWORD': os.environ.get('DATABASES_DEFAULT_PASSWORD', ''),
        'HOST': os.environ.get('DATABASES_DEFAULT_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DATABASES_DEFAULT_PORT', '5432',),
    }
}

# Email Settings
# https://docs.djangoproject.com/en/2.0/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
# EMAIL_PORT = os.environ.get('EMAIL_PORT', 465)
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', False)
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_SSL', False)

# Deployment

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'  # Default: 'SAMEORIGIN'

# HTTPS
# https://docs.djangoproject.com/en/dev/howto/deployment/checklist/#https

# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True

# Performance optimizations
# https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/#performance-optimizations

# CONN_MAX_AGE = None

# Fab commands configuration

WORKING_DIR = "www/{{project_name}}"
HOST_USER = ""
HOST_IP = ""
HOST_PORT = "22"
