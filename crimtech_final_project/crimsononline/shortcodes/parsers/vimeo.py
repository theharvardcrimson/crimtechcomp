from django.template.loader import render_to_string


def parse(kwargs, count=0):
    template_name = 'shortcodes/vimeo.html'

    video_id = kwargs.get('id')
    size = kwargs.get('size', 'medium')
    pos = kwargs.get('align', 'left')
    caption = kwargs.get('caption', None)
    if video_id:
        ctx = {
            'video_id': video_id,
            'size': size,
            'pos': pos,
            'caption': caption
        }
        return render_to_string(template_name, ctx)
    else:
        return ''
