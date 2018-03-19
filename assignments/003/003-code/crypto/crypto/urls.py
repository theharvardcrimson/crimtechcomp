from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from encode import urls as encode_urls
from decode import urls as decode_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'crypto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^encode/.*', include(encode_urls)),
    url(r'^decode/.*', include(decode_urls)),
    url(r'^.*', TemplateView.as_view(template_name='home.html')),
]
