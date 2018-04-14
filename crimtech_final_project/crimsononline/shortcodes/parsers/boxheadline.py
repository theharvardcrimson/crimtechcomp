from django.conf import settings
from django.template.loader import render_to_string

from crimsononline.content.models import Article


# I'm basing my code off of pullquote.py
def parse(kwargs):
    data = {}
    """
        Required: ArticleID
    """
    data['size'] = kwargs.get('size', 'medium')
    data['pos'] = kwargs.get('pos', 'left')
    data['font'] = kwargs.get('font', "'Crimson', Georgia, serif")
    # my things
    data['image'] = kwargs.get('image', None)

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

    return render_to_string('shortcodes/boxheadline.html', data)
