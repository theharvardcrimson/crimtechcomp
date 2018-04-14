from django.conf import settings
from django.template.loader import render_to_string


def parse(kwargs):
    data = {}

    data['text'] = kwargs.get('text')
    if data['text'] is None:
        if settings.TEMPLATE_DEBUG:
            raise Exception('Text not provided to textmod shortcode')
        else:
            return ''

    data['header'] = kwargs.get('header')
    if data['header'] is None:
        if settings.TEMPLATE_DEBUG:
            raise Exception('Header not provided to textmod shortcode')
        else:
            return ''

    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'medium')
    data['font'] = kwargs.get('font', "'Crimson', Georgia, serif")

    return render_to_string('shortcodes/textmod.html', data)
