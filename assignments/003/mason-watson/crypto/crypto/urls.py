from django.conf.urls import include, url
from django.contrib import admin
from decode import urls as decode_urls
from encode import urls as encode_urls
from crypto.views import *
urlpatterns = [
    # Examples:
    # url(r'^$', 'crypto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^encode/', include("encode.urls")),
    url(r'^decode/', include("decode.urls")),
    url(r'^.*', index),
]
