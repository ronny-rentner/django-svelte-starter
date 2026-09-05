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
    'backend.core',

    'django_vite',
    'jazzmin',

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
    'backend.core',
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

ROOT_URLCONF = 'backend.config.urls'

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

WSGI_APPLICATION = 'backend.config.wsgi.application'


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


###########
# JAZZMIN #
###########

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": f"{PROJECT_NAME} Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": f"{PROJECT_NAME} Admin",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": f"{PROJECT_NAME} Admin",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "src/assets/logo.svg",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "src/assets/logo.svg",

    # Logo to use for login form in dark themes (defaults to login_logo)
    #"login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "logo",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": f"Welcome to the {PROJECT_NAME} Admin",

    # Copyright on the footer
    "copyright": PROJECT_NAME,

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    "search_model": ["core.Person"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Dashboard",  "url": "admin:index", "permissions": ["auth.view_user"], "new_window": False},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User", "new_window": False},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        #{"name": "Auth", "app": "auth", "new_window": False},
    ],

    "usermenu_links": [
        {"model": "auth.user", "new_window": False}
    ],

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["core", "auth"],

    # Custom icons for side menu apps/models See: https://fontawesome.com/icons?d=gallery&m=free
    "icons": {
        "core.person": "fas fa-walking",
        "core.contactmessage": "fas fa-envelope",
        "core.youtubevideo": "fab fa-youtube",
        "core.youtubetranscript": "fab fa-youtube",
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },

    "default_icon_parents": "fas fa-circle-chevron-right",
    "default_icon_children": "fas fa-caret-square-right",

    # Use modals instead of popups
    "related_modal_active": True,

    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": "admin/custom.css",
    "custom_js": "admin/custom.js",
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": False,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    # Change view

    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "default",
    "dark_mode_theme": None,
    "actions_sticky_top": True,
    #"sidebar_nav_compact_style": True,
}

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
    'backend.core.authentication.TokenBackend',
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
    'backend': {
        'level': 'DEBUG',
        #'propagate': False,
    },
    #'cities_light': {
    #    'handlers':['console'],
    #    'propagate': True,
    #    'level':'DEBUG',
    #},
}
