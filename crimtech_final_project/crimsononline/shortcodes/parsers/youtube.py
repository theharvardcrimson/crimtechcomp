import urllib

from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string

DEFAULT_YOUTUBE_PARAMS = {
    # Slide player controls out of view automatically.
    'autohide': 1,

    # De-emphasize YouTube branding.
    'modestbranding': 1,

    # Don't show related videos after playback.
    'rel': 0,
}


def parse(kwargs):
    id = kwargs.get('id')
    size = kwargs.pop('size', 'medium')
    align = kwargs.pop('align', 'left')
    caption = kwargs.pop('caption', None)
    autoplay = kwargs.pop('autoplay', None)

    youtube_api_id = 'youtube-' + id

    # Assume any remaining kwargs are YouTube params.
    youtube_params = DEFAULT_YOUTUBE_PARAMS.copy()
    youtube_params.update(kwargs)
    youtube_params['playerapiid'] = youtube_api_id

    context = Context({
        'id': id,
        'size': size,
        'pos': align,
        'caption': caption,
        'autoplay': autoplay,
        'youtube_api_id': youtube_api_id,
        'youtube_params': urllib.urlencode(youtube_params)})

    if id:
        return render_to_string('shortcodes/youtube.html', context)
    elif settings.TEMPLATE_DEBUG:
        raise Exception('Youtube shortcode missing ID')
    else:
        return ''
