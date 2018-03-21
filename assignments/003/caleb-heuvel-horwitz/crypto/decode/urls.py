from django.conf.urls import url
from decode.views import *

urlpatterns = [
    url(r'^.*', index, name='index'),
]