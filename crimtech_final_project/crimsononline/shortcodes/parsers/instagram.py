from django.template.loader import render_to_string
from django.utils.html import strip_tags


def parse(kwargs):
    data = {}
    data['id'] = strip_tags(kwargs.get('id'))
    data['pos'] = strip_tags(kwargs.get('align', 'center'))
    data['size'] = strip_tags(kwargs.get('size', 'medium'))

    return render_to_string('shortcodes/instagram.html', data)
