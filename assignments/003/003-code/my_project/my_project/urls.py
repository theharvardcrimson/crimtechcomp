from django.conf.urls import include, url
from django.contrib import admin

from my_app import urls as my_app_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'my_project.views.home', name='home'),
    
    url(r'^', include('my_app_urls')),
    url(r'^admin/', include(admin.site.urls)),
]
