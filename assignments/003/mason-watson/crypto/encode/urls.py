from django.conf.urls import include, url
urlpatterns = [
    # Examples:
    # url(r'^$', 'crypto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^.*', encode_view)
]
