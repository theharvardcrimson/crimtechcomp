from django.conf.urls import include, url
from django.contrib import admin
from encode import urls as encode_urls
from decode import urls as decode_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'crimson.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^encode/.*', encode_urls),
    url(r'^decode/.*', decode_urls),
]
