from django.conf.urls import url

from my_app.views import *

urlpatterns = [
    url(r'^.*', index, name="index"),
]
