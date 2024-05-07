"""
Django settings for GMS_proj project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = 'C:\\images_gms'
MEDIA_URL = '/media/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0wud*nioem&x!*_-@2=c$q#4k%0*d0zj^k&w-04k)89_n2y(gp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.AppConfig',
    'shared_model',
    

    
    
    
   
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

ROOT_URLCONF = 'GMS_proj.urls'
# Set APP_DIRS to True to enable template discovery within app directories
APP_DIRS = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        os.path.join(BASE_DIR, 'user/templates/user'),  # Template directory for the 'user' app
        os.path.join(BASE_DIR, 'backoffice/templates'),  # Template directory for the 'backoffice' app
            # Add more template directories if needed
        ],
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

WSGI_APPLICATION = 'GMS_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cms',          # Your database name
        'USER': 'root_admin', # Your MySQL username
        'PASSWORD': 'root_admin', # Your MySQL password
        'HOST': '65.1.148.87',    # Your MySQL host
        'PORT': '3306',         # Your MySQL port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'user/static')]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    #social app custom setings
    # 'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    
]

# OAUTH2_PROVIDER = {
#     'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'openid': 'OpenID scope'},
#     'CLIENT_ID_GENERATOR_CLASS': 'oauth2_provider.generators.ClientIdGenerator',
#     'CLIENT_SECRET_GENERATOR_CLASS': 'oauth2_provider.generators.ClientSecretGenerator',
# }

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '121742523439-s30kcv1je7lg798uen7rd4ntk1oagh39.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# LOGIN_REDIRECT_URL = 'user:login_with_google'
# #LOGIN_REDIRECT_URL = '/user/dashboard/'

# # settings.py

# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

