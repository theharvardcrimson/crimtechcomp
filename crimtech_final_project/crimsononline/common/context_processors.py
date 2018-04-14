import datetime
import logging

from django.conf import settings

from crimsononline.newsletter.models import HarvardTodayNewsletter

logger = logging.getLogger(__name__)


def analytics(request):
    return {'ANALYTICS_USER_AGENT': settings.ANALYTICS_USER_AGENT}


def disqus(request):
    return {'DISQUS_SHORTNAME': settings.DISQUS_SHORTNAME}


def harvard_today(request):
    harvard_today = HarvardTodayNewsletter.objects.order_by(
        '-send_date').filter(send_date__lte=datetime.date.today()).first()
    return {
        'harvard_today': harvard_today
    }
