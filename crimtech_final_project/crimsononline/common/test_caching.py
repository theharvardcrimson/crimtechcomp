from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.utils.cache import get_cache_key
from django.views.decorators.cache import cache_page

from crimsononline.common import caching


def hello_world_view(request, value):
    return HttpResponse('Hello World %s' % value)


@override_settings(EXPIRE_CACHE_HOSTS=['testhost', 'testhost2'])
class ViewCacheExpirationTestCase(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_expire_page(self):
        cached_view = cache_page(3)(hello_world_view)

        # Construct two requests for the same view with different hosts and
        # schemes, since each absolute URI is individually cached.
        request_a = self.factory.get('/view/')
        request_a.META['HTTP_HOST'] = settings.EXPIRE_CACHE_HOSTS[0]

        request_b = self.factory.get('/view/')
        request_b.META['HTTP_HOST'] = settings.EXPIRE_CACHE_HOSTS[1]
        request_b._get_scheme = lambda: 'https'

        # Ensure our cache is empty to start.
        self.assertFalse(get_cache_key(request_a) in cache)
        self.assertFalse(get_cache_key(request_b) in cache)

        # Hit our view and assert we cache the request.
        cached_view(request_a, 1)
        self.assertTrue(get_cache_key(request_a) in cache)
        cached_view(request_b, 1)
        self.assertTrue(get_cache_key(request_a) in cache)

        # Expire the view by path and assert all cache entries with that path
        # are deleted.
        caching.expire_page('/view/')
        self.assertFalse(get_cache_key(request_a) in cache)
        self.assertFalse(get_cache_key(request_b) in cache)
