from django.template.loader import render_to_string


def parse(kwargs):
    display = kwargs.get('display', 'true')

    if display.lower() == 'false':
        return ''
    else:
        return render_to_string('shortcodes/media_inset.html')
