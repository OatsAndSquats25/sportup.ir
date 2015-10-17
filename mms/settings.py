"""
Django settings for mms project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

#########
# PATHS #
#########
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Full filesystem path to the project.
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = BASE_DIR.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, *MEDIA_URL.strip("/").split("/"))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

# Put strings here, like "/home/html/django_templates"
# or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (os.path.join(BASE_DIR, "templates"),)


############
# Settings #
############
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '!1e4g5lrbsif^992(qj!enn=h-fthd08h+)lukfn_c^vt2t*%d'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# TEMPLATE_DEBUG = True
# ALLOWED_HOSTS = []
SITE_ID=1

# Application definition
INSTALLED_APPS = (
    'theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.redirects',
    'django.contrib.gis',
    'rest_framework',
    'polymorphic',
    'generic',
    'flatpages',
    'accounts',
    'directory',
    'agreement',
    'program',
    'programcourse',
    'programsession',
    'enroll',
    'finance',
    'access',
    #'suds',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.i18n",
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.debug',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication',),
}

ROOT_URLCONF = 'mms.urls'
WSGI_APPLICATION = 'mms.wsgi.application'
#######################
# Internationalization#
#######################
# https://docs.djangoproject.com/en/1.6/topics/i18n/
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = "fa"
# Supported languages
LANGUAGES = (
    ('fa', 'Farsi'),
    #('en','English'),
)

TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

##################
# LOCAL SETTINGS #
##################
# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
DEBUG_APPS = (None,)
try:
    from local_settings import *
    INSTALLED_APPS += DEBUG_APPS
except ImportError as e:
    if "local_settings" not in str(e):
        raise e


#####################
# Default Variables #
#####################
REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
AUTH_USER_MODEL = 'auth.User'
AUTHENTICATION_BACKENDS = ('accounts.backends.EmailAuthBackend',)

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}

