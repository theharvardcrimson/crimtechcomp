import logging

from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import Image

logger = logging.getLogger(__name__)


def parse(kwargs):
    logger.debug('Parsing slider')
    old_id = kwargs.get('left_image')
    new_id = kwargs.get('right_image')

    data = {}
    try:
        data['left_image'] = Image.objects.get(pk=old_id)
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception(
                'The image with id {} was not found'.format(old_id))
        else:
            return ''

    try:
        data['right_image'] = Image.objects.get(pk=new_id)
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception(
                'The image with id {} was not found'.format(new_id))
        else:
            return ''
    data['size'] = kwargs.get('size', 'medium')
    data['byline'] = kwargs.get('byline', 'true').lower() == 'true'
    data['pos'] = kwargs.get('align', 'left')
    caption = kwargs.get('caption', 'false')

    if caption.lower() == 'true':
        data['caption'] = data['right_image'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption

    old_c = set([c.id for c in data['left_image'].contributors.all()])
    new_c = set([c.id for c in data['right_image'].contributors.all()])

    if old_c == new_c:
        data['num_bylines'] = 1
    else:
        data['num_bylines'] = 2

    return render_to_string('shortcodes/slider.html', data)
