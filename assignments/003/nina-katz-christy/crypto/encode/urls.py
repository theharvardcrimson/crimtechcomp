from django.conf.urls import include, url
from django.contrib import admin
from encode.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'crimson.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^.*', encode_view, name="encode_view"),
]
