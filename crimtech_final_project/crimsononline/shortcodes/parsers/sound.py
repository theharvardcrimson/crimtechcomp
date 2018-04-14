import re

from django.template.loader import render_to_string


def parse(kwargs):
    data = {}
    data['url'] = kwargs.get('url')
    data['id'] = re.findall(r'^.*/([^/]*?)$', data['url'])[0] or 0
    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'medium')

    return render_to_string('shortcodes/sound.html', data)
