from pathlib import Path
import os

from django.urls import reverse_lazy
from environs import Env


env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("DJANGO_SECRET", 'django-insecure-=ym7$patbmn#x2-9a%lkk3uq!8ymmob8y=5#z3j0z$$#5el1=z')
DEBUG = env.bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", ["*"])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # зависимости
    "django_seed",
    'mptt',

    # свои приложения
    'employees',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'employee_directory.urls'

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

WSGI_APPLICATION = 'employee_directory.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': env("DB_ENGINE", 'django.db.backends.postgresql'),
        'HOST': env('DB_HOST'),
        'PORT': env.int('DB_PORT'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
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
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'users.User'
LOGIN_URL = reverse_lazy("users:login")
LOGIN_REDIRECT_URL = reverse_lazy("employees:employees_list")
LOGOUT_REDIRECT_URL = reverse_lazy("users:login")


MPTT_DEFAULT_LEVEL_INDICATOR = '--'


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
