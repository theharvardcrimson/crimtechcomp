import copy

from django import template
from django.conf import settings
from django.core.urlresolvers import NoReverseMatch, reverse
from django.template.loader import get_template

register = template.Library()


class SectionLinkNode(template.Node):
    FORMAT = '<a href="{url}">{section}</a>'
    FORMAT_ACTIVE = '<a href="{url}" class="active">{section}</a>'

    def __init__(self, section, current_section):
        self.section = section.strip("\"\'")  # strip single and double quotes
        self.current_section = template.Variable(current_section)

    def render(self, context):
        try:
            url = reverse('content.section.' + self.section.lower())
        except NoReverseMatch:
            return ''  # abort if we can't link anywhere

        try:
            self.current_section = self.current_section.resolve(context)
        except template.VariableDoesNotExist:
            self.current_section = ''
        if self.current_section == self.section.lower():
            link = self.FORMAT_ACTIVE
        else:
            link = self.FORMAT

        return link.format(section=self.section, url=url)


@register.simple_tag(takes_context=True)
def render(context, model, method='default', **kwargs):
    """Includes a template based on model name and optional method

    Takes any number of keyword arguments that are added to the
    rendered template's context.

    Usage:

        {% render model [method] [additional=variables] %}

    Examples:

        {% render article %}
        {% render video "small" class="big" %}
    """
    try:
        model_name = model.__class__.__name__.lower()
        template_name = 'models/{}/{}.html'.format(model_name, method)
        context = copy.copy(context)
        context.update(kwargs)
        context[model_name] = model
        t = get_template(template_name)
        return t.render(context)
    except template.TemplateSyntaxError as e:
        if settings.DEBUG:
            return '[Rendered template had syntax error: %s]' % e
        else:
            return ''
    except template.TemplateDoesNotExist as e:
        if settings.DEBUG:
            return '[Rendered template does not exist: %s]' % e
        else:
            return ''


@register.simple_tag
def scalebox(imgs, elem, end_height):
    """
    Takes a set of pictures or things with main_rel_content and preserves
    their ratios when stretching the set of them to a certain height. Returns
    the height of `imgs[elem]` when stretching imgs to `end_height`.

    Usage: {% scalebox pics_array index_of_pic_in_consideration end_height %}
    """
    try:
        heights = []
        for i in imgs:
            if i.content_type.name == 'image':
                heights.append(float(i.pic.height) / i.pic.width)
            elif i.main_rel_content.content_type.name == 'image':
                heights.append(float(i.main_rel_content.pic.height) /
                               i.main_rel_content.pic.width)
            elif (i.main_rel_content.main_rel_content.content_type.name ==
                  'image'):
                j = i.main_rel_content.main_rel_content
                heights.append(float(j.pic.height) / j.pic.width)

        full_height = sum(heights)
        this_height = heights[elem]

        ratio = this_height / full_height

        return str(ratio * end_height)
    except:
        return '0'


@register.tag
def section_link(parser, token):
    """Generates link tags to content sections

    If optional current_section parameter is provided, the `active`
    class is applied to the link tag.

    Usage:

        {% section section_title [is current_section] %}

    Examples:

        {% section 'news' %}
        {% section 'arts' is current_section %}
    """
    args = token.split_contents()
    if len(args) == 2:
        tag_name, section_title = args
        current_section = None
    elif len(args) == 4 and args[2] == 'is':
        tag_name, section, sep, current_section = args
    else:
        raise template.TemplateSyntaxError(
            "%s tag must be of the form 'section \"section_title\""
            " [is current_section]'" % args[0])

    return SectionLinkNode(section, current_section)
