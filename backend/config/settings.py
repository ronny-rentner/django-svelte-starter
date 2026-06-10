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
DEBUG = True

DJANGO_VITE_DEV_MODE = DEBUG

CONFIG_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CONFIG_DIR.parent
BASE_DIR = BACKEND_DIR.parent
PROJECT_NAME = BASE_DIR.name

# Used to generate external links, e. g. for the invitation email.
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:5173')
FRONTEND_URL_EMAILS = config('FRONTEND_URL_EMAILS', default='http://localhost:8000')
FRONTEND_API_URL = config('FRONTEND_API_URL', default='http://localhost:8000/api')
RECAPTCHA_SITE_KEY = config('RECAPTCHA_SITE_KEY', default='starter-dev-recaptcha-key')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-i$r0^3%d)v4n6p$tb+qrww70ocsoc3w_11vi&61l*u=f#*_d21')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost', 'berlincube.ddnss.de', 'yuna.fritz.box', '192.168.178.60', 'host.docker.internal'])


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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Sets the etag http header
    'django.middleware.http.ConditionalGetMiddleware',


    # Set cors http headers
    'corsheaders.middleware.CorsMiddleware',

    # Static file serving as early as possible (but not before security)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static/collected'

if DEBUG:

    STATICFILES_DIRS = (
        BASE_DIR / 'static/src',
        BASE_DIR / 'static/frontend',
        ('src/assets', BASE_DIR / 'frontend/src/assets'),
    )

    DJANGO_VITE_ASSETS_PATH = BASE_DIR / "static" / "frontend"
    DJANGO_VITE_MANIFEST_PATH = BASE_DIR / "static/frontend/manifest.json"

else:

    DJANGO_VITE_ASSETS_PATH = STATIC_ROOT
    DJANGO_VITE_MANIFEST_PATH = STATIC_ROOT / 'manifest.json'

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
