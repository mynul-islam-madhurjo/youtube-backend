"""
Django settings for youtube_bff project.
Updated for YouTube Clone BFF API
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',           # Django REST Framework
    'corsheaders',             # CORS headers for frontend communication
    
    # Local apps
    'api',                     # Our YouTube API app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',        # CORS - must be at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'youtube_bff.urls'

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

WSGI_APPLICATION = 'youtube_bff.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Static files directories - This will serve files from the root static folder
STATICFILES_DIRS = [
    os.path.join(BASE_DIR.parent.parent, 'static'),  # Points to root/static/
]

# Media files (for uploaded content) - Use MEDIA_ROOT for uploaded files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ================================
# CORS CONFIGURATION FOR FRONTEND
# ================================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",     # Next.js default port
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

# During development, you can use this (less secure)
# CORS_ALLOW_ALL_ORIGINS = True

# ================================
# DJANGO REST FRAMEWORK SETTINGS
# ================================
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',  # For file uploads
        'rest_framework.parsers.FormParser',       # For form data
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024  # 100MB

# Video Upload Configuration
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB max video size
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

# Video storage paths - Use MEDIA_ROOT for uploaded files
VIDEO_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'videos')
THUMBNAIL_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'thumbnails')

# Ensure directories exist
os.makedirs(VIDEO_UPLOAD_PATH, exist_ok=True)
os.makedirs(THUMBNAIL_UPLOAD_PATH, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR.parent.parent, 'static', 'videos'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR.parent.parent, 'static', 'thumbnails'), exist_ok=True)
