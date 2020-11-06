import logging.config
import os
import sys


def get(variable):
    """
    To be used over os.environ.get() to avoid deploying local/dev keys in production. Forced
    env vars to be present.
    """
    if variable not in os.environ:
        raise Exception('Required environment variable not set: {}'.format(variable))

    return os.environ.get(variable)


# ==================================================================================================
# DJANGO SETTINGS
# ==================================================================================================


DEV = 'dev'
STAGING = 'staging'
PRODUCTION = 'production'
TESTING = 'test' in sys.argv
ENV = get('DJANGO_ENV')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('/project', '')
SECRET_KEY = get('SECRET_KEY')
DEBUG = False if ENV == PRODUCTION else True
ALLOWED_HOSTS = get('ALLOWED_HOSTS')

AUTH_USER_MODEL = 'user.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'adminsortable2',
    'corsheaders',
    'django_extensions',
    'django_filters',
    'djrichtextfield',
    'facebook',
    'mptt',  # Needed for 'apps.cms'
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_tracking',
    'workers',

    'apps.cms',
    'apps.file',
    'apps.logging',
    'apps.mail',
    'apps.socialmedia',
    'apps.user',
    'apps.webhook',

    # ___CHANGEME___
    # Example apps
    'apps.workerexample',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

if ENV in [STAGING, PRODUCTION]:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=500),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'django',  # ___CHANGEME___
            'USER': 'postgres',
            'PASSWORD': 'postgres'
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
        'level': 'WARNING',
        'handlers': ['console', 'sentry'],
    },
    'formatters': {
        'custom': {
            'format': '%(levelname)s %(message)s (in %(module)s.%(funcName)s:%(lineno)s by %(name)s)',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'custom'
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
    'loggers': {
        'apps': {'level': 'DEBUG'},
        'project': {'level': 'DEBUG'},
        'libs': {'level': 'DEBUG'},
        'django': {'level': 'INFO'},
        'gunicorn': {'level': 'WARNING'},
        'workers': {'level': 'DEBUG'}
    }
}
logging.config.dictConfig(LOGGING)


# ==================================================================================================
# 3RD PARTY SETTINGS
# ==================================================================================================


CORS_ORIGIN_ALLOW_ALL = True

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
        # SessionAuthentication may interfere with mobile API requests. If you are experiencing ssues, try commenting out the following line.
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

DJRICHTEXTFIELD_CONFIG = {
    'js': ['//cdn.quilljs.com/1.3.6/quill.js'],
    'css': {
        'all': [
            '//cdn.quilljs.com/1.3.6/quill.snow.css',
            'cms/css/admin.css',
        ]
    },
    'init_template': 'editor/init_quill.js',
    'settings': {
        'modules': {
            'toolbar': [
                [{'header': [1, 2, 3, False]}],
                ['bold', 'italic', 'underline'],
                [{'list': 'ordered'}, {'list': 'bullet'}],
                ['image', 'blockquote', 'code-block'],
                [{'align': []}],
                ['clean']
            ],
            'history': {
                'delay': 2000,
                'maxStack': 500,
                'userOnly': True
            }
        },
        'placeholder': 'Compose an epic...',
        'theme': 'snow'
    }
}

AWS_ACCESS_KEY_ID = get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get('AWS_STORAGE_BUCKET_NAME')
AWS_LOCATION = get('AWS_LOCATION')
AWS_DEFAULT_REGION = get('AWS_DEFAULT_REGION')
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False


# ==================================================================================================
# PROJECT SETTINGS
# ==================================================================================================


APP_NAME = '___CHANGEME___'
ADMIN_TITLE = 'Admin'
ADMIN_HEADER = 'Admin'

# Files
# Default to local uploads
LOCAL_FILE_UPLOADS = os.environ.get('LOCAL_FILE_UPLOADS', 'True') == 'True'
if not LOCAL_FILE_UPLOADS:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Enable file resize task by uncommenting the task decorator for apps.file.tasks.resize_images()
FILE_IMAGE_RESIZE_SCHEDULE = 60  # How often to check for images to resizes (in seconds)
FILE_IMAGE_SIZES = (
    {'key': 'th', 'width': 350, 'quality': 90},
    {'key': 'md', 'width': 800},
)


# Facebook Login
FACEBOOK_GRAPH_VERSION = '3.1'
FACEBOOK_APP_ID = get('FACEBOOK_APP_ID')
FACEBOOK_APP_CLIENT_TOKEN = get('FACEBOOK_APP_CLIENT_TOKEN')
FACEBOOK_APP_SECRET = get('FACEBOOK_APP_SECRET')
# This must match the URL specified in the Facebook app login settings "Valid OAuth Redirect URIs"
FACEBOOK_SUCCESSFUL_LOGIN_URL = get('FACEBOOK_SUCCESSFUL_LOGIN_URL')

# Google Login
GOOGLE_CLIENT_ID = get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = get('GOOGLE_CLIENT_SECRET')
GOOGLE_SUCCESSFUL_LOGIN_URL = get('GOOGLE_SUCCESSFUL_LOGIN_URL')
GOOGLE_PROJECT_ID = get('GOOGLE_PROJECT_ID')
GOOGLE_REDIRECT_URI = get('GOOGLE_REDIRECT_URI')

# MAIL
SEND_MAIL = get('SEND_MAIL') == 'True'
EMAIL_PROVIDER = os.environ.get('EMAIL_PROVIDER', 'smtp')  # 'smtp' or 'sendgrid'

WEB_URL = get('WEB_URL')
RESET_PASSWORD_URL = '{}{}'.format(WEB_URL, '/reset-password/{reset_token}/{user_id}')
DEFAULT_FROM_EMAIL = '___CHANGEME___@example.org'
DEFAULT_FROM_NAME = '___CHANGEME___'

if EMAIL_PROVIDER == 'smtp':
    EMAIL_HOST = get('SMTP_SERVER')
    EMAIL_HOST_USER = get('SMTP_LOGIN')
    EMAIL_HOST_PASSWORD = get('SMTP_PASSWORD')
    EMAIL_PORT = os.environ.get('SMTP_PORT', 587)
    EMAIL_USE_TLS = True

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_URL = 'https://api.sendgrid.com/v3/mail/send'

# Webhooks
WEBHOOKS_NOTIFY_URL = os.environ.get('WEBHOOKS_NOTIFY_URL')
