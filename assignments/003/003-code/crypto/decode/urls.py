from django.conf.urls import url

from decode.views import *

urlpatterns = [
    url(r'^.*', decode_view, name="decode_view"),
]