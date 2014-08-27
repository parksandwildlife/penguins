import dj_database_url
import ldap
import os

from django_auth_ldap.config import (LDAPSearch, GroupOfNamesType,
                                     LDAPSearchUnion)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True #os.environ.get('DEBUG', False)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']
#INTERNAL_IPS = ('*',) #'127.0.0.1',)

# Email settings
ADMINS = ('asi@dpaw.wa.gov.au',)
EMAIL_HOST = 'alerts.corporateict.domain'
EMAIL_PORT = 25

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
    'gunicorn',
    'django_nose',
    'rest_framework',
    'leaflet',
    # actual app
    'observations'
)

ANONYMOUS_USER_ID=1

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
)

ROOT_URLCONF = 'penguins.urls'

WSGI_APPLICATION = 'penguins.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {'default': dj_database_url.config()}
CONN_MAX_AGE = None

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
SITE_ID = 1
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Perth'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
#import ipdb; ipdb.set_trace()

if os.environ.get('USE_AWS', False):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_HOST = os.environ['AWS_S3_HOST']

FLATPAGES_X_PARSER= ["flatpages_x.markdown_parser.parse", {}]

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "observations", "templates"),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'swingers.sauth.backends.EmailBackend',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL_FAILURE = LOGIN_URL
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = LOGOUT_URL
ANONYMOUS_USER_ID = -1

# LDAP settings
AUTH_LDAP_SERVER_URI = os.environ.get('LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = os.environ.get('LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD')

AUTH_LDAP_ALWAYS_UPDATE_USER = False
AUTH_LDAP_AUTHORIZE_ALL_USERS = True
AUTH_LDAP_FIND_GROUP_PERMS = False
AUTH_LDAP_MIRROR_GROUPS = False
AUTH_LDAP_CACHE_GROUPS = False
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch("DC=corporateict,DC=domain", ldap.SCOPE_SUBTREE,
               "(sAMAccountName=%(user)s)"),
    LDAPSearch("DC=corporateict,DC=domain", ldap.SCOPE_SUBTREE,
               "(mail=%(user)s)"),
)

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "DC=corporateict,DC=domain",
    ldap.SCOPE_SUBTREE, "(objectClass=group)"
)

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: False,
    ldap.OPT_REFERRALS: False,
}

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': "givenName",
    'last_name': "sn",
    'email': "mail",
}

# Misc settings
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)

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
APPLICATION_VERSION_NO = '0.1a'

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    #'django_jenkins.tasks.django_tests',   # select one django or
    #'django_jenkins.tasks.dir_tests'      # directory tests discovery
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    #'django_jenkins.tasks.run_jslint',
    #'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_sloccount',
    #'django_jenkins.tasks.lettuce_tests',

)


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
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
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/penguins.log'),
            'formatter': 'standard',
            'maxBytes': '16777216'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'video_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/videos.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'observations': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        },
        'videos': {
            'handlers': ['console', 'video_file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

if DEBUG:
    # Set up logging differently to give us some more information about what's
    # going on
    LOGGING['loggers'] = {
        'django_auth_ldap': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'observations': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        },
        'videos': {
            'handlers': ['console', 'video_file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
