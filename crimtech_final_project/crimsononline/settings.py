# flake8: noqa
"""
Django settings for crimsononline project.


FOR THE SITE TO WORK, YOU NEED TO CREATE A LOCAL SETTINGS FILE FIRST
use `sample_local_settings.py` as a template
"""

import os

from easy_thumbnails.conf import Settings as easy_thumbnails_defaults
from PIL import ImageFile

ImageFile.MAXBLOCK = 1024*1024


DEBUG = True

TEMPLATE_DEBUG = DEBUG

USE_TZ = True

READ_ONLY = False
READ_ONLY_CONTACT = 'Nikhil Benesch (585-755-1570)'

_PROJECT_ROOT = os.environ.get('X_DJANGO_PROJECT_PATH', os.path.normpath(os.path.join(os.path.realpath(os.path.dirname(__file__)), '..')))
_APP_ROOT = os.path.normpath(os.path.join(_PROJECT_ROOT, '..', '..'))

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

SITE_ID = 1

ADMINS = ()

MANAGERS = ADMINS

INTERNAL_IPS = ()

GEOIP_PATH = '/srv/crimson/geoip'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.thecrimson.com']

EXPIRE_CACHE_HOSTS = ['www.thecrimson.com']

DEVELOPMENT_HOSTS = ['local.thecrimson.com', '127.0.0.1:8000', 'localhost:8000']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crimson',
        'USER': 'crimson',
        'PASSWORD': 'crimson',
        'HOST': 'localhost',
        'PORT': '',
    }
}

ROOT_URLCONF = 'crimsononline.urls'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    os.path.join(_PROJECT_ROOT, 'crimsononline', 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(_PROJECT_ROOT, 'crimsononline', 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'crimsononline.common.context_processors.analytics',
    'crimsononline.common.context_processors.disqus',
    'crimsononline.common.context_processors.harvard_today',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
    'crimsononline.newsletter.middleware.NewsletterSubscribeMiddleware'
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin.apps.SimpleAdminConfig',
    'django.contrib.redirects',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'crimsononline.content',
    'crimsononline.shortcodes',
    'crimsononline.placeholders',
    'crimsononline.admin_cust',
    'crimsononline.ads',
    #'crimsononline.content_module',
    'crimsononline.common',
    'crimsononline.imageuploader',
    'crimsononline.search',
    'crimsononline.march_madness',
    'crimsononline.archive_photos',
    'crimsononline.newsletter',
    'redactor',
    'crimsononline.texteditors',
    'social.apps.django_app.default',
    'sortedm2m',
    'storages',
    'easy_thumbnails',
    'django_extensions',
    'solo',
    'compressor',
    'djcelery',
    'django_select2',
]

MEDIA_URL = 'https://s3.amazonaws.com/media.thecrimson.com/'

STATIC_URL = 'https://s3.amazonaws.com/static.thecrimson.com/'

STATICFILES_STORAGE = 'crimsononline.common.storage.CachedS3BotoStaticStorage'
COMPRESS_STORAGE = STATICFILES_STORAGE

COMPRESS_OFFLINE = True

DEFAULT_FILE_STORAGE = 'crimsononline.common.storage.S3MediaStorage'

THUMBNAIL_DEFAULT_STORAGE = 'crimsononline.common.storage.S3ThumbnailStorage'
THUMBNAIL_MEDIA_ROOT = 'https://s3.amazonaws.com/thumbnails.thecrimson.com/'
THUMBNAIL_MEDIA_URL = 'https://s3.amazonaws.com/thumbnails.thecrimson.com/'

DOCS_ROOT = os.path.join(_PROJECT_ROOT, 'docs', '_build', 'html')

AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_STATIC_STORAGE_BUCKET_NAME = 'static.thecrimson.com'
AWS_MEDIA_STORAGE_BUCKET_NAME = 'media.thecrimson.com'
AWS_THUMBNAIL_STORAGE_BUCKET_NAME = 'thumbnails.thecrimson.com'
AWS_S3_CALLING_FORMAT = 'boto.s3.connection.OrdinaryCallingFormat'
AWS_S3_CALLING_FORMAT_STATIC = 'boto.s3.connection.OrdinaryCallingFormat'

# NEEDS S3 KEYS!! (provide in local_settings.py)

DOWNLOAD_UPSTREAM_MEDIA = False
UPSTREAM_MEDIA_URL = ''

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

THUMBNAIL_QUALITY = 95

THUMBNAIL_PROCESSORS = easy_thumbnails_defaults.THUMBNAIL_PROCESSORS + (
    'crimsononline.content.templatetags.content_filters.gradient_processor',
)

# caching durations in sec
CACHE_SHORT = 2 * 60 * 60
CACHE_STANDARD = 4 * 60 * 60
CACHE_LONG = 12 * 60 * 60
CACHE_EONS = 7 * 24 * 60 * 60

if DEBUG:
    CACHE_BACKEND = 'dummy:///'
    CACHE_MIDDLEWARE_SECONDS = 5

ANALYTICS_USER_AGENT = 'UA-327124-1'

# whether to use Sentry for error reporting (DSN defined in local_settings)
CRIMSON_USE_SENTRY = False

# send contact form FROM this address
# (Amazon SES needs the sender address to be at a verified domain)
CONTACT_FORM_SENDER_ADDRESS = 'president@thecrimson.com'
ADMISSIONS_BLOG_ADDRESS = 'admissions@thecrimson.com'

DISQUS = True
DISQUS_SHORTNAME = 'thecrimson'

GOOGLE_CUSTOM_SEARCH_ENGINE_ID = '018182123538720087896:jxrddb2lgiy'

FLYBY_TIP_ADDRESS = 'flybytips@thecrimson.com'

MAILCHIMP_API_KEY = '588342403be5880c4fdd692dc0083f32-us6'
MAILCHIMP_WEBHOOK_KEY = '82923fDSKJFST322385uFKEHF25873rh'


# Notifies the users in "to" whenever someone edits an article over
# "time_span" days old"
NOTIFY_ON_SKETCHY_EDIT = {
    'enabled': False,
    'from': 'businessmanager@thecrimson.com',
    'to': ['president@thecrimson.com'],
    'subject': 'Sketchy Article Change!',
    'time_span': 7,  # In days
}

# Break this out here to avoid circular import of urls.py
# XXX Having this here is totally incorrect. Move this. --NB
CONTENT_URL_RE = r'(?P<ctype>[\w\-]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/' \
                 '(?P<day>\d{1,2})/(?P<slug>[0-9\w_\-%]+)/$'
CGROUP_URL_RE = r'(?P<gtype>[\w]+)/(?P<gname>[\w0-9\-]+)/'
CGROUP_FILTER_URL_RE = r'(page/(?P<page>\d+)/)?(tags/(?P<tags>[,\w&\'\s-]+)/)?'

# sponcon1 url finder that hides the publication date
SPONSORED_CONTENT_URL_RE = r'(?P<ctype>[\w\-]+)/(?P<slug>[0-9\w_\-%]+)/$'

if DEBUG:
    SECRET_KEY = 'Saaob)kz,u>LuIsyPk#2FfbzwlwdS^R/VFWL^1.GA9QYB>mDWY'
    URL_BASE = '/'

ADS_USER_ID = '1046082'

DFP_HEADERS = {
    'applicationName': 'The Harvard Crimson',
    'clientSecret': 'Jp14XrKt-DAKhn2YCPahmLel',
    'networkCode': ADS_USER_ID,
    'refreshToken': '1/JRRYJgH9M-4zJbviwwXstcO5Yb59sTUM2xLvs8s0PfE',
    'clientId': '267453316523-6ch72ll2gkamfkqltgabsirreho138nq.apps.googleusercontent.com',
}

DFP_CONFIG = {
    'request_log': 'n',
    'log_home': os.path.join(_APP_ROOT, 'logs'),
    'xml_parser': '2',
    'xml_log': 'n',
    'debug': 'n',
    'home': _APP_ROOT
}

# Settings for secured Google Analytics API calls
# Yes, this is probably the worst possible way to store a private key. Get
# over it. It can't be used for anything besides read-access to analytics
ANALYTICS_CONFIG = {
    'private_key_id': 'c6a9dc660cf3b820d359043fb7fc2d4629e52cf8',
    'private_key': '-----BEGIN PRIVATE KEY-----\n'
                   'MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAMAPYVfrbIGjQ8bw\n'
                   '5ObEHJ6v2A3pvCds0K/A3kJA98w/t2mcwEHukRmFuUsTv3v2oOsGRCsDEgn2crKW\n'
                   'JK3H2S6Ttmp0Zt59SQo9axSARzn0ikokzDKIaIlCEnqGl0OjKNBNMq3CoE5oZT2q\n'
                   '4n60yrI+LTGophL6E+sqJAJjBuDDAgMBAAECgYBuJ2QZXPl60P0KmRdwE4KmsQwl\n'
                   'zq0Pn6WBaAkRztlQ2CqF9FWAeyfVj5DaspTcsHNS2OE4Gia6eBMIwnx+/2RcB8mh\n'
                   'OuxG2f83wQCShhR44BwgqVJSZkI/JoFop+RLyCNe6CC+PQCOnDbPfZieVehkIxEc\n'
                   'ArU0fn6EXLZIilqzIQJBAOkEoEsN5oevwNi1aFJEcM4kniNf3wUPeQAYquIcIrqP\n'
                   'yPpBOZEQsZBxyud4n1tA2Tud96xlzCJ+0C1hCwegTw8CQQDTAJ+M0+cpkFbSk9Am\n'
                   'Oe6hzMfIhR53rwE28E8hMRXDas3fWskR8LxUtokZf/d/MlSBSMF98gqAYprsq5xV\n'
                   'r1MNAkA/qy7tMxAhVQl5bR/jEqZL/T9kZQa4CEFEoHjYrV1j4nPExVuoYopR8HXD\n'
                   'h3brZS22F3ScG3iKmGHjdFeiLtBLAkBw0Vd9s9tYZN2XUAMuPTFzf4uekladBYxv\n'
                   'tIOKqrUJPHUBJIh3uDDqVoLtiHdrohx+18jlL2IgDRjqzEMVqV2NAkApV2LvehTu\n'
                   'ShIee/DOOKnshCuki0ikXTaLXoKNmLaS03LmgfS4JWn9RpOBjgTwmk0yU75RjW5s\n'
                   '61P729GCMacE\n'
                   '-----END PRIVATE KEY-----\n',
    'client_email': '181309082208-qcr2jvekce1pokmrmh02u5t86njr0nd4@developer.gserviceaccount.com',
    'client_id': '181309082208-qcr2jvekce1pokmrmh02u5t86njr0nd4.apps.googleusercontent.com',
    'type': 'service_account'
}

# Default auth group for @thecrimson.com accounts on admin
SOCIAL_AUTH_BASEUSER = 'Crimed'

# Redirection settings for python-social-auth
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGIN_ERROR_URL = '/'

SOCIAL_AUTH_WHITELISTED_DOMAINS = ['thecrimson.com']

AUTH_EXTRA_ARGUMENTS = {'prompt': 'select_account'}

# IMPORTANT NOTE:
#
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
# must be defined in local_settings.py

# Pipeline for python-social-auth.
SOCIAL_AUTH_PIPELINE = (
    'crimsononline.admin_cust.pipeline.force_new_user',
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'crimsononline.admin_cust.pipeline.update_permissions',
    'social.pipeline.user.user_details',
)

AUTHENTICATION_BACKENDS = (
  # 'social.backends.google.GoogleOpenId',
  'social.backends.google.GoogleOAuth2',
  'django.contrib.auth.backends.ModelBackend',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

try:
    from local_settings import *
except ImportError:
    pass

# Note: all code below this point is here for a reason - they depend on
# variables being set in local_settings.py

COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT

if CRIMSON_USE_SENTRY:
    INSTALLED_APPS = INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',
    ]

if DEBUG:
    INSTALLED_APPS += [
        'kombu.transport.django',
    ]

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
    'ANALYTICS_USER_AGENT': ANALYTICS_USER_AGENT,
    'DISQUS_SHORTNAME': DISQUS_SHORTNAME,
}

REC_ARTICLES = {
    'NUM_REC_ARTICLES': 5,  # Number of recommended content to generate
    'NUM_KEYWORDS': 8,      # Number of keywords to store
    'MAX_KW_COMBO': 5,      # Maximum size of keyword combination
    'MIN_KW_COMBO': 1,      # Minimum size of keyword combination
    'CORPUS_SIZE': 10000,   # Number of articles to use to populate Word table
    'ACCEPT_PROB': .1,      # Probability of accepting old articles
    'RECENCY_CUTOFF': 5     # Age cutoff (years) to trigger ACCEPT_PROB
}
