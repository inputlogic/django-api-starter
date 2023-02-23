import logging.config
import os
import sys

from celery.schedules import crontab
import django_heroku


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

# Admin Banner
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
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

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'ERROR',
        'handlers': ['console'],
    },
    'formatters': {
        'custom': {
            'format': '%(levelname)s %(message)s (in %(module)s.%(funcName)s:%(lineno)s by %(name)s)',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'custom'
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


WORKERS_SLEEP = 1
WORKERS_PURGE = 1000

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

APP_NAME = 'Dev App'  # ___CHANGEME___
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
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Enable file resize task by uncommenting the task decorator for apps.file.tasks.resize_images()
FILE_IMAGE_RESIZE_SCHEDULE = 60  # How often to check for images to resizes (in seconds)
FILE_IMAGE_SIZES = (
    {'key': 'th', 'width': 350, 'quality': 90},
    {'key': 'md', 'width': 800},
)


# ==================================================================================================
# EMAIL SETTINGS
# ==================================================================================================


DEFAULT_FROM_EMAIL = 'hello@inputlogic.ca'  # ___CHANGEME___
DEFAULT_FROM_NAME = 'Input Logic Dev'  # ___CHANGEME___

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
CELERY_RESULT_EXTENDED = True
CELERY_BEAT_SCHEDULE = {
    'example-seconds': {
        'task': 'apps.user.tasks.example_scheduled_task',
        'schedule': 60.0,  # Call every 60 seconds
    },
    'example-cron': {
        'task': 'apps.user.tasks.example_scheduled_task',
        'schedule': crontab(minute=0, hour=0)  # Call at midnight every day
    }
}


# ==================================================================================================
# HEROKU & GITHUB
# ==================================================================================================

if ENV in [STAGING, PRODUCTION]:
    django_heroku.settings(locals(), staticfiles=False)

if TESTING:
    try:
        del DATABASES['default']['OPTIONS']['sslmode']
    except KeyError:
        pass
