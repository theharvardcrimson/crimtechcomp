from django.conf.urls import include, url
from django.contrib import admin

from my_app import urls as my_app_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'assignment.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^authors', include(my_app_urls)),
    url(r'^articles', include(my_app_urls)),
    url(r'^', include(my_app_urls)),
]
