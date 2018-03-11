from django.conf.urls import url
from django.contrib import admin

from encode import urls as encode_urls
from decode import urls as decode_urls

urlpatterns = [
    url(r'^encode/.*', encode_urls),
    url(r'^decode/.*', decode_urls)
]
