import logging.config
import os
import sys

import dj_database_url


# ==================================================================================================
# CHANGE FIELDS
# ==================================================================================================


APP_NAME = 'Dev App'
DEFAULT_FROM_EMAIL = 'hello@inputlogic.ca'
DEFAULT_FROM_NAME = 'Input Logic Dev'


# ==================================================================================================
# ENVIRONMENT SETTINGS
# ==================================================================================================


DEV = 'dev'
STAGING = 'staging'
PRODUCTION = 'production'
TEST = 'test'
ENV = os.environ.get('DJANGO_ENV', DEV)
TESTING = 'test' in sys.argv or ENV == TEST
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG' if ENV == DEV else 'WARNING')


# ==================================================================================================
# DJANGO SETTINGS
# ==================================================================================================


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('/project', '')
SECRET_KEY = os.environ.get('SECRET_KEY', 'local')
DEBUG = False if ENV == PRODUCTION else True
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

AUTH_USER_MODEL = 'user.User'

INSTALLED_APPS = [
    # Custom Admin settings (must be before django.contrib.admin)
    'django_admin_env_notice',
    'admin_interface',
    'colorfield',

    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    # 3rd party
    'django_celery_results',
    'django_extensions',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',

    # Local
    'apps.file',
    'apps.mail',
    'apps.user',
]

MIDDLEWARE = [
    'libs.corsmiddleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_admin_env_notice.context_processors.from_settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

if ENV in (STAGING, PRODUCTION):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'django'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        },
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# ==================================================================================================
# ADMIN SETTINGS
# ==================================================================================================


# Set Django admin banner colour based on environment
if ENV == DEV:
    ENVIRONMENT_NAME = "Development Environment"
    ENVIRONMENT_COLOR = "#828282"
elif ENV == STAGING:
    ENVIRONMENT_NAME = "Staging Staging Environment"
    ENVIRONMENT_COLOR = "#FF2222"
else:
    ENVIRONMENT_NAME = None
    ENVIRONMENT_COLOR = None


# ==================================================================================================
# LOGGING
# ==================================================================================================


LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG' if ENV == DEV else 'WARNING')
LOG_APPNAME = os.environ.get('LOG_APPNAME', 'DJANGO')
LOG_SYSNAME = f'{APP_NAME}-{ENV.upper()}'
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'ERROR',
        'handlers': ['console', 'papertrail'],
    },
    'formatters': {
        'custom': {
            'format': '\
                %(levelname)s %(message)s \
                (in %(module)s.%(funcName)s:%(lineno)s by %(name)s)',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
        },
        'simple': {
            'format': f'\
                %(asctime)s {LOG_SYSNAME} {LOG_APPNAME} \
                [%(process)d]: %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'custom'
        },
        'papertrail': {
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'simple',
            'address': ('logs7.papertrailapp.com', 52333)
        },
    },
    'loggers': {
        'apps': {'level': LOG_LEVEL},
        'libs': {'level': LOG_LEVEL},
        'project': {'level': LOG_LEVEL},
        'django': {'level': 'INFO' if ENV == DEV else 'WARNING'},
        'gunicorn': {'level': 'WARNING'},
    }
}
logging.config.dictConfig(LOGGING)


# ==================================================================================================
# 3RD PARTY SETTINGS
# ==================================================================================================


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # SessionAuthentication may interfere with mobile API requests.
        # If you are experiencing ssues, try commenting out the following line.
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'EXCEPTION_HANDLER': 'libs.exception_handler.exception_handler'
}

ADMIN_TITLE = 'Admin'
ADMIN_HEADER = 'Admin'

WEB_URL = os.environ.get('WEB_URL', 'http://localhost:3000')
RESET_PASSWORD_URL = '{}{}'.format(WEB_URL, '/reset-password/{reset_token}/{user_id}')


# ==================================================================================================
# FILE SETTINGS
# ==================================================================================================


AWS_ACCESS_KEY_ID = os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID')
AWS_DEFAULT_REGION = os.environ.get('BUCKETEER_AWS_REGION')
AWS_SECRET_ACCESS_KEY = os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('BUCKETEER_BUCKET_NAME')
AWS_LOCATION = ''
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

if AWS_ACCESS_KEY_ID:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Enable file resize task by uncommenting the task decorator for apps.file.tasks.resize_images()
FILE_IMAGE_RESIZE_SCHEDULE = 60  # How often to check for images to resizes (in seconds)
FILE_IMAGE_SIZES = (
    {'key': 'th', 'width': 350, 'quality': 90},
    {'key': 'md', 'width': 800},
)


# ==================================================================================================
# EMAIL SETTINGS
# ==================================================================================================


EMAIL_HOST = os.environ.get('SMTP_SERVER', 'smtp.postmarkapp.com')
EMAIL_PORT = os.environ.get('SMTP_PORT', 587)
EMAIL_HOST_USER = os.environ.get('SMTP_USERNAME', None)  # Required, add to Heroku config or .env file
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD', None)  # Required, add to Heroku config or .env file
EMAIL_USE_TLS = True

SEND_MAIL = True if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD else False


# ==================================================================================================
# REDIS
# ==================================================================================================


REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_DB = os.environ.get('REDIS_DB', 0)
REDIS_URL = os.environ.get('REDIS_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')


# ==================================================================================================
# CELERY / WORKERS
# ==================================================================================================


CELERY_BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ALWAYS_EAGER = TESTING  # Process tasks inline (no queue) if we're in test mode
CELERY_RESULT_EXTENDED = True  # Provide more data in Django Admin results

# Example of how to schedule tasks
# =================================
# from celery.schedules import crontab  # Import at top of file
#
#  CELERY_BEAT_SCHEDULE = {
#      'example-seconds': {
#          'task': 'apps.user.tasks.example_scheduled_task',
#          'schedule': 60.0,  # Call every 60 seconds
#      },
#      'example-cron': {
#          'task': 'apps.user.tasks.example_scheduled_task',
#          'schedule': crontab(minute=0, hour=0)  # Call at midnight every day
#      }
#  }


# ==================================================================================================
# GITHUB
# ==================================================================================================


if TESTING:
    try:
        del DATABASES['default']['OPTIONS']['sslmode']
    except KeyError:
        pass
