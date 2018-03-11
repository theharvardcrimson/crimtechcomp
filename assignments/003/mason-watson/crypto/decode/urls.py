from django.conf.urls import include, url
from decode.views import *

urlpatterns = [
    url(r'^.*', decode_view)
]
