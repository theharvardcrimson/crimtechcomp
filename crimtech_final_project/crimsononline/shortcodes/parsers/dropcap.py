from django.conf import settings
from django.template.loader import render_to_string


def parse(kwargs):
    data = {}

    data['text'] = kwargs.get('text', '')
    data['color'] = kwargs.get('color', None)

    if not data['text']:
        if settings.TEMPLATE_DEBUG:
            raise Exception('No text provided to dropcap shortcode')
        else:
            return ''

    return render_to_string('shortcodes/dropcap.html', data)
