from django.conf.urls import url
from encode.views import *

urlpatterns = [
    url(r'^.*', encode_view),
]