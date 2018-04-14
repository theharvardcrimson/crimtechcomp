# flake8: noqa

import os

DEBUG = True

TEMPLATE_DEBUG = True

_APP_ROOT = '/srv/crimson'

ADMINS = (
)

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

MANAGERS = ADMINS

# disable caching
CACHE_SHORT = 1
CACHE_STANDARD = 1
CACHE_LONG = 1
CACHE_EONS = 1

# Uncomment this to turn on caching:
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': 'localhost:11211',
#     }
# }

try:
    ALLOWED_HOSTS += ['.elb.amazonaws.com', ]
except NameError:
    ALLOWED_HOSTS = ['.thecrimson.com', 'elb.amazonaws.com']

ALLOWED_HOSTS += ['localhost']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'crimson',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'lite': {
            'format': '[%(asctime)s - %(name)s:%(lineno)s]: %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
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
            'class': 'logging.FileHandler',
            'filename': '/srv/crimson/log/django.log',
            'formatter': 'lite',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'crimsononline': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'wsgi': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pick_50_random_chars_3oif3jfawfjpj8FJ#F$IOF2392!#t'


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(_APP_ROOT, 'uploads')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

DOWNLOAD_UPSTREAM_MEDIA = True  # indicates whether to try to pull down images
UPSTREAM_MEDIA_URL = 'http://media.thecrimson.com/'  # production media url

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
THUMBNAIL_MEDIA_ROOT = os.path.join(_APP_ROOT, 'uploads', 'thumbnails')

# Save static files on local server rather than S3
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
COMPRESS_STORAGE = 'compressor.storage.CompressorFileStorage'

COMPRESS_ROOT = '/srv/crimson/releases/current/static'
STATIC_ROOT = os.path.join(_APP_ROOT, 'static')
STATIC_URL = '/static/'

AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

BROKER_URL = 'django://'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '49299719815-7m6h4b4ioca8nibfflvov4suuakvat4d.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'rPLWDWR-H0s0hLhOQEzJl2VT'

DISQUS_USER_KEY = 'vabqI2su93P1wVF3Ls9kXhXhRggV7y2ylokjq137yPAz47cY5dDMHgUA2QlZoWNE'
DISQUS_FORUM_KEY = 'pkUMj0suYbfCUXu2hon1EB5xrgMLWADS9kNZiGtJ0ISE76QLyMvEb2SyPFmS3F5x'
DISQUS_FORUM_ID = '1508'

DISQUS_SHORTNAME = 'thecrimson-dev'

ANALYTICS_USER_AGENT = 'UA-327124-11'
GOOGLE_API_KEY = 'ABQIAAAAdoBgu2mGyHlwNmFWklwtOBSMTarlKQyRRh5ucdthk06p19vF5xQFCzYsXKd1Wl-sgDQvPuCHDW3o8A'

SITE_ID = 2

ISSUU_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ISSUU_API_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
