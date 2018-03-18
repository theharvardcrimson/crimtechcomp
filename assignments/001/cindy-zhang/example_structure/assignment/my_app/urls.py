from django.conf.urls import url
from my_app.views import *

urlpatterns = [
    url(r'articles', articles, name='articles'),
    url(r'authors', author, name='authors'),
    url(r'^', index, name='index'),
]
