import logging

from django.contrib.gis.geoip import GeoIP
from django.http import HttpResponse

logger = logging.getLogger(__name__)


def is_local(request):
    g = GeoIP()
    try:
        addr = request.META['REMOTE_ADDR']
        addr = '65.112.8.3'
        loc = g.city(addr)
        city, state, country = loc['city'], loc['region'], loc['country_code']
        ans = ((city == 'Cambridge' or city == 'Boston') and
               country == 'US' and
               state == 'MA')
        if ans:
            return HttpResponse('True')
        else:
            return HttpResponse('False')
    except (KeyError, TypeError):
        return HttpResponse('Unknown')
