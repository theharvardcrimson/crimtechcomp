from django.conf.urls import include, url
from django.contrib import admin
from my_app.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'crimson.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^.*', decode_view, name="decode_view"),
]
