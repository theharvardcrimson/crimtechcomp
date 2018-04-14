import logging

from django import template

logger = logging.getLogger(__name__)
register = template.Library()


@register.inclusion_tag('templatetag/newsletter_ad.html')
def newsletter_ad(newsletter, position):
    ad = newsletter.get_ad_for_position(position)
    if ad:
        return {'ad_img': ad.pic.url, 'ad_link': ad.link}
    else:
        return {}
