"""
Django settings for AuthService project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

## TEST MODE
# LOCAL_TEST : TEST CODE 작성시
# LOCAL : 로컬 서버 돌릴 때 
# PRODUCTION : 배포용
MODE = "PRODUCTION"

# SECURITY WARNING: keep the secret key used in production secret!
if MODE=="LOCAL_TEST" or MODE=='LOCAL':
    SECRET_KEY = "django-insecure-h!ojgwre1e58)16&bmuve3mn#dnll#dt&eoo14!rq2s3bffkn2"
else: # MODE = PRODUCTION
    SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if MODE == 'PRODUCTION':
    ALLOWED_HOSTS = ["*"]
else: # MODE = LOCAL or LOCAL_TEST
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'sharedb',
    'user',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

SOCIALACCOUNT_LOGIN_ON_GET = True

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


ROOT_URLCONF = 'AuthService.urls'

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

WSGI_APPLICATION = 'AuthService.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

''' # sqlite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'db.sqlite3',
    }
}
'''

# PostgreSQL
if MODE == 'PRODUCTION':
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("PRODUCTION_ENGINE"),
            'NAME': os.environ.get("PRODUCTION_NAME"), # Schema Name
            'USER': os.environ.get("PRODUCTION_USER"),
            'PASSWORD': os.environ.get("PRODUCTION_PASSWORD"), # PASSWORD
            'HOST':os.environ.get("PRODUCTION_HOST"),
            'PORT':os.environ.get("PRODUCTION_PORT"),
        }
    }
# NOT TESTING MODE
else: # MODE=LOCAL
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("DB_ENGINE"),
            'NAME': os.environ.get("DB_NAME"), # Schema Name
            'USER': os.environ.get("DB_USER"),
            'PASSWORD': os.environ.get("DB_PASSWORD"), # PASSWORD NAME
            'HOST':os.environ.get("DB_HOST"),
            'PORT':os.environ.get("DB_PORT"),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# social app custom settings
# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',
                        # 'allauth.account.auth_backends.AuthenticationBackend'                
# ]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [ # 기본적인 view 접근 권한 지정
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [ # session 혹은 token을 인증 할 클래스 설정
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PARSER_CLASSES': [ # request.data 속성에 액세스 할 때 사용되는 파서 지정
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ]
}

AUTH_USER_MODEL = "sharedb.User"


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
