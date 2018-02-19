from django.conf.urls import url
from my_app.views import *

urlpatterns = [
    url(r'authors', authors, name='authors'),
    url(r'articles', articles, name='articles'),
    url(r'^', index, name='index'),
]
