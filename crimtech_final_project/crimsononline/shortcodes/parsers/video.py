from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import Video


def parse(kwargs):
    id = kwargs.get('id')

    data = {}

    try:
        data['video'] = Video.objects.get(pk=id)
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception('Video with id %d not found or unpublished', id)
        else:
            return ''

    data['id'] = data['video'].key
    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'medium')
    data['byline'] = kwargs.get('byline', 'false').lower() == 'true'
    caption = kwargs.get('caption', 'false')
    if caption.lower() == 'true':
        data['caption'] = data['video'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption

    return render_to_string('shortcodes/youtube.html', data)
