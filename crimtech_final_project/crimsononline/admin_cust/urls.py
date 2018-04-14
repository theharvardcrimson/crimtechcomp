from django.conf import settings
from django.conf.urls import include, url

from . import admin, views

if settings.READ_ONLY:
    urlpatterns = [
        url(r'^', views.offline),
    ]
else:
    urlpatterns = [
        url(r'^', include(admin.site.urls)),
    ]
