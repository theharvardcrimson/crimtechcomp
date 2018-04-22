from django.conf.urls import include, url
from django.contrib import admin
import encode.urls as encode_urls
import decode.urls as decode_urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'crypto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^encode/', include(encode_urls)),
    url(r'^decode/', include(decode_urls)),
    url(r'^.*', include(encode_urls))
]
