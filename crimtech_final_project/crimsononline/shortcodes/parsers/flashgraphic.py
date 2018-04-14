from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import FlashGraphic


def parse(kwargs):
    id = kwargs.get('id')

    data = {}

    try:
        data['flashgraphic'] = FlashGraphic.objects.get(pk=id)
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception(
                'Flash Graphic with id %d not found or unpublished' % id)
        else:
            return ''

    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'medium')
    data['height'] = kwargs.get('height', '300')
    data['byline'] = kwargs.get('byline', 'false').lower() == 'true'
    caption = kwargs.get('caption', 'false')
    if caption.lower() == 'true':
        data['caption'] = data['flashgraphic'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption

    return render_to_string('shortcodes/flashgraphic.html', data)
