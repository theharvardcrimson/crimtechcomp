from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import Article


# I'm basing my code off of pullquote.py
def parse(kwargs):
    data = {}
    """
        Required: Text Speaker Title(Linked Article Title)
    """
    data['text'] = kwargs.get('text')
    if data['text'] is None:
        if settings.TEMPLATE_DEBUG:
            raise Exception('Text not provided to pullquote shortcode')
        else:
            return ''

    data['image'] = kwargs.get('image', None)

    data['size'] = kwargs.get('size', 'medium')
    data['pos'] = kwargs.get('pos', 'left')
    data['font'] = kwargs.get('font', "'Crimson', Georgia, serif")
    # my things
    data['speaker'] = kwargs.get('speaker', None)
    # description is the part that comes after the speaker.
    # Like, "Drew Faust, PRESIDENT OF HARVARD"
    data['description'] = kwargs.get('description', None)

    sc_id = kwargs.get('id', None)
    # getting related content
    if sc_id:
        try:
            data['relContent'] = Article.objects.get(pk=sc_id)
        except:
            if settings.TEMPLATE_DEBUG:
                raise Exception(
                    'Content with id ' + sc_id + ' not found or unpublished')
            else:
                return ''
    else:
        data['relContent'] = None

    return render_to_string('shortcodes/boxquote.html', data)
