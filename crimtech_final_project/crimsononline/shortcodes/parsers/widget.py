import logging
import re

from django.template.loader import render_to_string

from crimsononline.content.models import Widget

logger = logging.getLogger(__name__)


def parse(kwargs, count=None):
    sc_id = kwargs.get('id')

    data = {}

    data['widget'] = Widget.objects.get(pk=sc_id)

    data['pos'] = kwargs.get('align', 'left')
    size = kwargs.get('size', 'medium')
    # small size aligns incorrectly
    data['size'] = 'medium' if size == 'small' else size
    data['byline'] = kwargs.get('byline', 'true').lower() == 'true'

    data['imports'] = ''
    # insert import statements for highcharts and google visualization
    if data['widget'].is_highcharts:
        data['imports'] += '{{ highcharts import }}'
    if data['widget'].is_d3:
        data['imports'] += '{{ d3 import }}'
    caption = kwargs.get('caption', 'false')
    if caption.lower() == 'true':
        data['caption'] = data['widget'].description
    elif caption.lower() == 'false':
        data['caption'] = None
    else:
        data['caption'] = caption

    return re.sub(
        r'\{\{\ *id *\}\}',
        'container' + str(count),
        render_to_string('shortcodes/widget.html', data))
