from hashlib import sha1

from django.conf import settings
from django.core.cache import cache as _djcache
from django.http import HttpRequest
from django.utils.cache import get_cache_key


def funcache(seconds=1800, prefix=''):
    """Cache the result of a function call for the specified number of seconds.

    Usage:

    @funcache(600)
    def myExpensiveMethod(parm1, parm2, parm3):
        ....
        return expensiveResult
    """
    def doCache(f):
        def x(*args, **kwargs):
            desc = [f.__module__, getattr(f, 'im_class', ''),
                    f.__name__, args, kwargs]
            key = sha1(''.join([str(x) for x in desc])).hexdigest()
            result = _djcache.get(key)
            if result is None:
                result = f(*args, **kwargs)
                _djcache.set(key, result, seconds)
            return result

        return x

    return doCache


# Path is something like /section/fm/
def expire_page(path):
    for scheme in ('http', 'https'):
        for host in settings.EXPIRE_CACHE_HOSTS:
            request = HttpRequest()
            request._get_scheme = lambda: scheme
            request.META['HTTP_HOST'] = host
            request.path = path
            key = get_cache_key(request)
            _djcache.delete(key)


def expire_all():
    _djcache.clear()
