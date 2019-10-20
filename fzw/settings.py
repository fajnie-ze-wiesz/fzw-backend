"""
Django settings for fzw project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'abracadabra')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', '0')))

BACKEND_HOST = os.environ.get('BACKEND_HOST', '*')
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgres://fajniezewiesz:fajniezewiesz@localhost:5432/fajniezewiesz')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')

FZW_ASSETS_S3_BUCKET = os.environ.get('FZW_ASSETS_S3_BUCKET')
FZW_MEDIA_S3_BUCKET = os.environ.get('FZW_MEDIA_S3_BUCKET')

ALLOWED_HOSTS = [
    BACKEND_HOST,
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'storages',

    'fzw.main',
    'fzw.news',
    'fzw.quizes',
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

ROOT_URLCONF = 'fzw.urls'

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

WSGI_APPLICATION = 'fzw.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa: E501
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_WHITELIST = [
    'localhost:8080',
    'wybornie.org:8080',

    'fajnie-ze-wiesz.github.io',
    'aplikacja.fajniezewiesz.pl',
    'app.fajniezewiesz.pl',

    'test-fajnie-ze-wiesz.github.io',
    'test-app.fajniezewiesz.pl',
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'  # noqa
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'fzw': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

USE_S3 = bool(AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY)


def s3_url(bucket_name):
    return f'https://{bucket_name}.s3-eu-west-1.amazonaws.com/'


if USE_S3 and FZW_ASSETS_S3_BUCKET:
    STATIC_URL = s3_url(FZW_ASSETS_S3_BUCKET)
    STATIC_ROOT = None
    STATICFILES_STORAGE = 'fzw.storage_backends.AssetsStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(DATA_DIR, 'assets')

if USE_S3 and FZW_MEDIA_S3_BUCKET:
    MEDIA_URL = s3_url(FZW_MEDIA_S3_BUCKET)
    MEDIA_ROOT = None
    DEFAULT_FILE_STORAGE = 'fzw.storage_backends.MediaStorage'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
