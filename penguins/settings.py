import dj_database_url
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ['SECRET_KEY'] if os.environ.get('SECRET_KEY', False) else 'foo'
S3_FOLDER = os.environ['S3_FOLDER'] if os.environ.get('S3_FOLDER', False) else 'foo'
DEBUG = True if os.environ.get('DEBUG', False) == 'True' else False
TEMPLATE_DEBUG = DEBUG
CSRF_COOKIE_SECURE = True if os.environ.get('CSRF_COOKIE_SECURE', False) == 'True' else False
SESSION_COOKIE_SECURE = True if os.environ.get('SESSION_COOKIE_SECURE', False) == 'True' else False

if not DEBUG:
    # Localhost, UAT and Production hosts
    ALLOWED_HOSTS = [
        'localhost',
        '.dpaw.wa.gov.au',
        '.dbca.wa.gov.au'
    ]
INTERNAL_IPS = ('127.0.0.1', '::1')

# Email settings
ADMINS = ('asi@dbca.wa.gov.au',)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'markitup',
    'flatpages_x',
    'sorl.thumbnail',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django_jenkins',
    'django_extensions',
    'debug_toolbar',
    'daterange_filter',
    'compressor',
    'datetimewidget',
    'south',
    'storages',
    'django_wsgiserver',
    'django_nose',
    'rest_framework',
    'leaflet',
    # actual app
    'observations'
)

ANONYMOUS_USER_ID = 1

AUTH_USER_MODEL = "observations.PenguinUser"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'penguins.context_processors.standard',
)

ROOT_URLCONF = 'penguins.urls'

WSGI_APPLICATION = 'penguins.wsgi.application'

# Database
DATABASES = {'default': dj_database_url.config()}
CONN_MAX_AGE = None

POSTGIS_VERSION = (2, 0, 3)

# Internationalization
SITE_ID = 1
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Perth'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

if os.environ.get('USE_AWS', False):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_HOST = os.environ['AWS_S3_HOST']
    AWS_QUERYSTRING_AUTH = False

FLATPAGES_X_PARSER = ["flatpages_x.markdown_parser.parse", {}]

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "observations", "templates"),
)

# Authentication
from ldap_email_auth import ldap_default_settings
ldap_default_settings()

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'ldap_email_auth.auth.EmailBackend')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = LOGIN_URL
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = LOGOUT_URL
ANONYMOUS_USER_ID = -1


# Misc settings

COMPRESS_ENABLED = False

MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_SKIN = 'markitup/skins/markitup'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': False})

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

LEAFLET_CONFIG = {
    'SCALE': 'metric',
}

DEBUG_TOOLBAR_CONFIG = {
    'HIDE_DJANGO_SQL': False,
    'INTERCEPT_REDIRECTS': False,
}

# Application version number
APPLICATION_VERSION_NO = '1.0'

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_sloccount',
)


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console': {'format': '%(asctime)s %(name)-12s %(message)s'},
        'standard': {
            'format': '%(asctime)-.19s [%(process)d] [%(levelname)s] '
                      '%(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'log': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'observations': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        },
        'videos': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

if DEBUG:
    # Set up logging differently to give us some more information about what's
    # going on
    LOGGING['loggers'] = {
        'django_auth_ldap': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'observations': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'videos': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
