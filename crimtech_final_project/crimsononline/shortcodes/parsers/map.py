from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import Map


def parse(kwargs):
    id = kwargs.get('id')

    data = {}

    try:
        data['map'] = Map.objects.get(pk=id)
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception(
                'Map with id ' + str(id) + ' not found or unpublished')
        else:
            return ''

    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'medium')
    data['byline'] = kwargs.get('byline', 'false').lower() == 'true'
    caption = kwargs.get('caption', 'false')
    if caption.lower() == 'true':
        data['caption'] = data['map'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption

    return render_to_string('shortcodes/map.html', data)
