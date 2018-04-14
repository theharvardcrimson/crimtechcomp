from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import Image


def parse(kwargs):
    sc_id = kwargs.get('id')

    data = {}

    try:
        data['image'] = Image.objects.get(pk=sc_id)
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception(
                'Image with id ' + sc_id + ' not found or unpublished')
        else:
            return ''

    data['nofilm'] = kwargs.get('nofilm', False)
    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'medium')
    data['byline'] = kwargs.get('byline', 'true').lower() == 'true'
    data['quote'] = kwargs.get('quote', False)
    data['quotebyline'] = kwargs.get('quotebyline', False)
    data['theme'] = kwargs.get('theme', 'light')
    caption = kwargs.get('caption', 'false')
    if caption.lower() == 'true':
        data['caption'] = data['image'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption

    return render_to_string('shortcodes/image.html', data)
