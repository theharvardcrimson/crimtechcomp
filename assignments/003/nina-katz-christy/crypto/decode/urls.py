from django.conf.urls import include, url
from django.contrib import admin
from decode.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'crimson.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^.*', decode_view, name="decode_view"),
]
