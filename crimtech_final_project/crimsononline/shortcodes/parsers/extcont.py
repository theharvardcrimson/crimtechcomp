from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import ExternalContent


def parse(kwargs):
    id = kwargs.get('id')

    data = {}
    try:
        data['ec'] = ExternalContent.objects.get(pk=id).child
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception(
                'ExternalContent with id %d not found or unpublished' % id)
        else:
            return ''

    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'medium')
    data['byline'] = kwargs.get('byline', 'true').lower() == 'true'
    caption = kwargs.get('caption', 'false')
    if caption.lower() == 'true':
        data['caption'] = data['ec'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption

    return render_to_string('shortcodes/extcont.html', data)
