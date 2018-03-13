from django.conf.urls import include, url
from django.contrib import admin

from encode import urls as encode_urls
from decode import urls as decode_urls
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'crypto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^encode/.*', include(encode_urls)),
    url(r'^decode/.*', include(decode_urls)),
    url(r'^.*', views.index, name="index"),
]
