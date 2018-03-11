from django.conf.urls import include, url
from encode.views import *
urlpatterns = [
    url(r'^.*', encode_view)
]
