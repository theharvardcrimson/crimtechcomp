from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^subscribe/online/$', views.subscribe_online),
    url(r'^subscribe/track/$', views.subscribe_track),
    url(r'^subscribe/(?:(?P<form_type>\w+)/)?$',
        views.SubscribeView.as_view()),
]
