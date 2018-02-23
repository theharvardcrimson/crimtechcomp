from django.conf.urls import url
from my_app.views import *

urlpatterns = [
    url(r'^', index, name='index'),
]


######

#guessing this below does the same work as what's above
#from django.urls import path

#from . import views

#urlpatterns = [
#    path('', views.index, name='index'),
#]
