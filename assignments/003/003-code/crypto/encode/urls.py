from django.conf.urls import url

from views import encode_view

urlpatterns = [
    url(r'^.*', encode_view, name="encode_view"),
]