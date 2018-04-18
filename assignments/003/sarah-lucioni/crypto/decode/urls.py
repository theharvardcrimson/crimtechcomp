from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'crypto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^.*', views.decode_view, name='decode_view')
]
