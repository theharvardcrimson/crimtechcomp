from django import template
from django.conf import settings

from ..models import AdUnit, AdZone

register = template.Library()


class AdUnitNode(template.Node):
    def __init__(self, size, is_mobile, dependent_el=None, size_cutoff=None):
        self.size = size
        self.is_mobile = is_mobile
        self.dependent_el = dependent_el
        self.size_cutoff = size_cutoff

    def render(self, context):
        ad_units = context['ad_units'] = context.get('ad_units', {})
        key = (self.size, self.is_mobile)
        if key not in ad_units:
            if not context.get('ad_zone'):
                context['ad_zone'] = 'content'
            placement_units = AdZone.objects.units_for_placement(
                zone_name=context.get('ad_zone'),
                size=self.size,
                mobile=self.is_mobile)
            ad_units[key] = list(placement_units)  # force evaluation

        if ad_units[key]:
            ad_unit = ad_units[key].pop(0)
            templ = template.loader.get_template('templatetags/ad_unit.html')
            subcontext = template.Context({'ad_unit': ad_unit,
                                           'dependent_el': self.dependent_el,
                                           'size_cutoff': self.size_cutoff})
            return templ.render(subcontext)
        else:
            return '<!-- no ad units available -->'


class OldAdUnitNode(template.Node):
    def __init__(self, code, width, height):
        self.code = code
        if self.code[0] == self.code[-1] and self.code[0] in ('"', "'"):
            self.code = self.code[1:-1]
        self.width = width
        self.height = height

    def render(self, context):
        ad_unit = {
            'code': self.code,
            'dimensions': (self.width, self.height),
            'mobile': 'false',
        }
        templ = template.loader.get_template('templatetags/ad_unit.html')
        subcontext = template.Context({'ad_unit': ad_unit})
        return templ.render(subcontext)


@register.tag
def ad_unit(parser, token):
    args = token.split_contents()

    if len(args) == 4:
        return OldAdUnitNode(args[1], args[2], args[3])

    if len(args) not in [2, 3, 5]:
        raise template.TemplateSyntaxError(
            "'ad_unit' tag requires two or three or five arguments")

    size = args[1]
    if not (size[0] == size[-1] and size[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "first 'ad_unit' argument (size) should be in quotes")
    size = size[1:-1]

    if len(args) == 3 and args[2] != 'mobile':
        raise template.TemplateSyntaxError(
            "second 'ad_unit' argument must be 'mobile' if present")
    is_mobile = (len(args) == 3)  # we just confirmed it's mobile

    if len(args) == 5:
        assert args[2] == '"new"'
        depel = args[3]
        if not (depel[0] == depel[-1] and depel[0] in ('"', "'")):
            raise template.TemplateSyntaxError(
                "first 'ad_unit' argument (depel) should be in quotes")
        depel = depel[1:-1]
        return AdUnitNode(size, False, depel, args[4])

    return AdUnitNode(size, is_mobile)


@register.inclusion_tag('templatetags/ads_head.html')
def ads_head():
    return {
        'ad_units': AdUnit.objects.all(),
        'user_id': settings.ADS_USER_ID
    }


# bRealTime changes by PN Remove when finished.
@register.inclusion_tag('templatetags/ads_head2.html')
def ads_head2():
    return {
        'ad_units': AdUnit.objects.all(),
        'user_id': settings.ADS_USER_ID
    }
