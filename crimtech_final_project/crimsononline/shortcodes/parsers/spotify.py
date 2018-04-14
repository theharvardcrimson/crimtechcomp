from django.conf import settings
from django.template.loader import render_to_string


def parse(kwargs):
    data = {}

    data['uri'] = kwargs.get('uri')
    if data['uri'] is None:
        if settings.TEMPLATE_DEBUG:
            raise Exception('Spotify uri not provided to spotify shortcode')
        else:
            return ''

    data['pos'] = kwargs.get('pos', 'left')
    data['size'] = kwargs.get('size', 'medium')
    data['compact'] = kwargs.get('compact', 'false').lower() == 'true'

    return render_to_string('shortcodes/spotify.html', data)
