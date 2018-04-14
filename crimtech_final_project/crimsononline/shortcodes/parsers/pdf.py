from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import PDF


def parse(kwargs):
    id = kwargs.get('id')

    data = {}
    try:
        data['pdf'] = PDF.objects.get(pk=id).child
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception('PDF with id %d not found or unpublished', id)
        else:
            return ''

    data['embed'] = kwargs.get('embed', 'True')
    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'large')
    data['height'] = kwargs.get('height', '500px')
    data['byline'] = kwargs.get('byline', 'false').lower() == 'true'
    caption = kwargs.get('caption', 'false')
    if caption.lower() == 'true':
        data['caption'] = data['pdf'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption
    data['STATIC_URL'] = settings.STATIC_URL
    return render_to_string('shortcodes/pdf.html', data)
