from django.template.loader import render_to_string


def parse(kwargs):
    data = {}
    data['id'] = kwargs.get('id')
    data['pos'] = kwargs.get('align', 'center')
    data['size'] = kwargs.get('size', 'medium')

    return render_to_string('shortcodes/tweet_timeline.html', data)
