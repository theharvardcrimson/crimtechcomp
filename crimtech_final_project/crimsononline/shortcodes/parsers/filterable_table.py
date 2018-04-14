import logging

from django.template.loader import render_to_string

from crimsononline.content.models import Table

logger = logging.getLogger(__name__)


def parse(kwargs, count=0):
    sc_id = kwargs.get('id')

    data = {}

    data['table'] = Table.objects.get(pk=sc_id)

    # Column to filter by. Defaults to first column
    data['filter_column'] = kwargs.get('filter_column', '0')

    data['size'] = kwargs.get('size', 'medium')
    data['pos'] = kwargs.get('pos', 'left')

    data['height'] = kwargs.get('height', '300')
    data['byline'] = kwargs.get('byline', 'true').lower() == 'true'

    caption = kwargs.get('caption', 'false')
    if caption.lower() == 'true':
        data['caption'] = data['table'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption

    data['count'] = count

    return render_to_string('shortcodes/filterable_table.html', data)
