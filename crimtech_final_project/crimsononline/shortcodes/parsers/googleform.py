from django.conf import settings
from django.template.loader import render_to_string


def parse(kwargs):
    data = {}

    # TODO make this an exception
    data['id'] = kwargs.get('id')
    if data['id'] is None:
        if settings.TEMPLATE_DEBUG:
            raise Exception('Id not provided to googleform shortcode')
        else:
            return ''

    data['pos'] = kwargs.get('pos', 'center')
    data['size'] = kwargs.get('size', 'medium')
    data['height'] = kwargs.get('height', 500)

    return render_to_string('shortcodes/googleform.html', data)
