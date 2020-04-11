"""
Django settings for medical_peek_api project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import pymysql
from core.utility.functional import select_keys


APP_LABEL = 'mp'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y-tuhir)&drs@w%r+(-le%rch@gu7nrvhng(0(m!(z(61(je0c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'jh6sghndhe.execute-api.us-east-1.amazonaws.com',
    'covid.callahanwilliam.com'
]

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_swagger',
    'django_s3_storage',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'medical_peek_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medical_peek_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'medical_peek_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

pymysql.install_as_MySQLdb()
pymysql.version_info = (1, 3, 13, 'final', 0)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, "medical_peek_api/resources/data_source.cnf"),
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'medical_peek_api/static')

STATIC_S3_BUCKET = 'medical.callahanwilliam.com'

STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
AWS_S3_BUCKET_NAME_STATIC = STATIC_S3_BUCKET

# These next two lines will serve the static files directly
# from the s3 bucket
AWS_S3_CUSTOM_DOMAIN = f'{STATIC_S3_BUCKET}.s3.amazonaws.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# File Uploads

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'medical.uploads.callahanwilliam.com'
AWS_DEFAULT_ACL = 'private'
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 3600
AWS_S3_ENCRYPTION = False

# Rest Framework

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    #
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.FileUploadParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# CORS

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'cache-control',
    'category',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'x-api-client'
)

# Logging

DEFAULT_LOG_HANDLERS = ['console']

ALL_LOG_HANDLERS = {
    'file': {
        'level': 'DEBUG',
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'formatter': 'verbose',
        'filename': os.path.join(BASE_DIR, 'medical_peek_api/resources/log/debug.log'),
        'when': 'midnight',
        'interval': 1,
        'backupCount': 0,
        'encoding': None,
        'delay': 0,
        'utc': False
    },
    'console': {
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'formatter': 'verbose'
    }
}

LOG_HANDLERS = select_keys(os.environ.get('LOG_HANDLERS', 'console').split(','), ALL_LOG_HANDLERS)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': LOG_HANDLERS,
    'loggers': {
        'axes.watch_login': {
            'handlers': DEFAULT_LOG_HANDLERS,
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': DEFAULT_LOG_HANDLERS,
            'level': 'INFO',
            'propagate': True,
        },
        'django.db': {
            'handlers': DEFAULT_LOG_HANDLERS,
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': DEFAULT_LOG_HANDLERS,
            'level': 'DEBUG',
            'propagate': False,
        },
        'medical_peek_api': {
            'handlers': DEFAULT_LOG_HANDLERS,
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'request_format': {
            'format': '%(remote_addr)s %(username)s "%(request_method)s '
                      '%(path_info)s %(server_protocol)s" %(http_user_agent)s '
                      '%(message)s %(asctime)s',
        },
        'verbose': {
            'format': '%(levelname)s - %(asctime)s - %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    }
}
