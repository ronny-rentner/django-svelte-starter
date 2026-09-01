import importlib
import os
from pathlib import Path

import ultraimport

from djultra.utils.config_loader import ConfigLoader
config = ConfigLoader()
config.config_file = config('CONFIG_FILE', default="/dev/null")

###########
# GENERAL #
###########

#os.environ["DJANGO_RUNSERVER_HIDE_WARNING"] = "true"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)

LOG_LEVEL = config('LOG_LEVEL', default="ERROR")

CONFIG_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CONFIG_DIR.parent
BASE_DIR = BACKEND_DIR.parent
PROJECT_NAME = BASE_DIR.name

# Frontend / API URLs, set per environment. They encode how the app is served — in
# dev the Django API (:8000) and Vite SPA (:5173) on separate ports, in production a
# single reverse-proxied origin. See the readme, "How the frontend and API are
# served". CORS_ALLOWED_ORIGINS and the CSP connect-src build on these.
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:5173')
FRONTEND_URL_EMAILS = config('FRONTEND_URL_EMAILS', default='http://localhost:8000')
FRONTEND_API_URL = config('FRONTEND_API_URL', default='http://localhost:8000/api')
# reCAPTCHA v3 — defaults to Google's universal test keys: they always validate
# (the widget shows a "for testing only" banner), so the contact/sign-in forms
# work out of the box. Set your real keys via env / CONFIG_FILE in production.
RECAPTCHA_SITE_KEY = config('RECAPTCHA_SITE_KEY', default='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY', default='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-i$r0^3%d)v4n6p$tb+qrww70ocsoc3w_11vi&61l*u=f#*_d21')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost', 'host.docker.internal', 'example.com'])


# Application definition

INSTALLED_APPS = [
    'core',

    'django_vite',
    #'jazzmin',

    'corsheaders',
    'rest_framework',
    'csp',

    'djultra',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'django_tasks',
    'django_tasks_db',
]

INSTALLED_ULTRA_APPS = [
    'core',
    'djultra',
]

TASKS = {
    "default": {
        "BACKEND": "django_tasks_db.DatabaseBackend",
        "QUEUES": []
    }
}

ARTIFICIAL_DELAY = {
    'path': '/api/',  # Path to delay (e.g., '/api/slow/')
    'delay': 5,       # Delay time in seconds
}

# djultra's injected app settings wrap this list with its own middleware
MIDDLEWARE = [
    # First in the list so its CORS headers survive on every outgoing
    # response, including the 304s that ConditionalGetMiddleware fabricates
    'corsheaders.middleware.CorsMiddleware',

    # Sets the etag http header
    'django.middleware.http.ConditionalGetMiddleware',

    'django.middleware.security.SecurityMiddleware',

    # Static file serving
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    # After the session is initialized, we can run our auth
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Set csp http headers
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [CONFIG_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            #'debug': False,
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ.get('DB_NAME',     'dss'),
        'USER':     os.environ.get('DB_USER',     'dss'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'dss'),
        'HOST':     os.environ.get('DB_HOST',     'localhost'),
        'PORT':     os.environ.get('DB_PORT',     '5433'),
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'


# Static files: STATIC_URL/STATIC_ROOT and the django-vite paths come from
# djultra's injected app settings (LOAD APP SETTINGS below)

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#####################
# LOAD APP SETTINGS #
#####################

# Import settings for all apps in `INSTALLED_ULTRA_APPS`
for app in INSTALLED_ULTRA_APPS:
    path = ultraimport.search_module_path(app)
    settings_file_path = f"{path}/settings.py"
    if os.path.exists(settings_file_path):
        app_settings = ultraimport(settings_file_path, '*', inject=globals(), add_to_ns=True)

########
# AUTH #
########

AUTHENTICATION_BACKENDS = [
    'core.authentication.TokenBackend',
    # For Django Admin
    'django.contrib.auth.backends.ModelBackend',
]

# Enables the user login API (sign-in request + token login). When False, those
# endpoints are not registered, so users cannot log in. Backend-only: it does not
# affect the models or the frontend.
USER_LOGIN_ENABLED = config('USER_LOGIN_ENABLED', default=True)

#########
# EMAIL #
#########

# In dev, log emails to the console instead of attempting SMTP delivery.
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

###########
# LOGGING #
###########

LOGGING['loggers'] |= {
    'django-svelte-starter': {
        'level': 'DEBUG',
        #'propagate': False,
    },
    #'cities_light': {
    #    'handlers':['console'],
    #    'propagate': True,
    #    'level':'DEBUG',
    #},
}
