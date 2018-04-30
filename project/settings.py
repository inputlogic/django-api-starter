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


DEV = 'dev'
PRODUCTION = 'production'
TESTING = 'test' in sys.argv
ENV = os.environ.get('DJANGO_ENV', DEV)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('/project', '')
SECRET_KEY = get('SECRET_KEY')
DEBUG = True if ENV is DEV else False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', ['*'])

AUTH_USER_MODEL = 'user.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'authtools',
    'corsheaders',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',

    'apps.user',
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
        'DIRS': [],
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

if ENV == PRODUCTION:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=500)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'django-starter',
            'USER': 'postgres',
            'PASSWORD': 'postgres'
        }
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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_METADATA_CLASS': 'drf_auto_endpoint.metadata.AutoMetadata',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # For browseable API
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'libs.permissions.IsOwnerOrReadOnly',
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

AWS_ACCESS_KEY_ID = get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get('AWS_STORAGE_BUCKET_NAME')
AWS_LOCATION = 'django-starter'
AWS_QUERYSTRING_AUTH = False

WEB_URL = get('WEB_URL')
RESET_PASSWORD_URL = '{web_url}/{path}'.format(
    web_url=WEB_URL,
    path='reset-password/{reset_token}/{user_id}'
)

SENDGRID_API_KEY = get('SENDGRID_API_KEY')
SENDGRID_TEMPLATE_NEW_ACCOUNT = get('SENDGRID_TEMPLATE_NEW_ACCOUNT')
SENDGRID_TEMPLATE_FORGOT_PASSWORD = get('SENDGRID_TEMPLATE_FORGOT_PASSWORD')

SEND_EVENTS = get('SEND_EVENTS') == 'True'
