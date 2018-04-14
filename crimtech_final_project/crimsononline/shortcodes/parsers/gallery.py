from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import Gallery


def parse(kwargs, count=0):
    id = kwargs.get('id')

    data = {}

    try:
        data['gallery'] = Gallery.objects.get(pk=id)
    except:
        if settings.TEMPLATE_DEBUG:
            raise Exception(
                'Gallery with id ' + str(id) + ' not found or unpublished')
        else:
            return ''

    inline = kwargs.get('inline', 0)
    if inline:
        data['inlines'] = data['gallery'].contents.all()[:inline]

    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'medium')
    data['caption'] = kwargs.get('caption')
    data['carousel'] = kwargs.get('carousel', 'false').lower() == 'true'
    data['sizespec'] = kwargs.get('sizespec', '1500,1500,1500,1500')
    data['byline'] = kwargs.get('byline', 'false').lower() == 'true'
    # needed because reasons:
    data['STATIC_URL'] = settings.STATIC_URL
    data['id'] = count

    return render_to_string('shortcodes/gallery.html', data)
