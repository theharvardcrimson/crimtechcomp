from django.conf.urls import include, url

urlpatterns = [
    url(r'^.*', decode_view)
]
