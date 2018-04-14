from django.template.loader import render_to_string


def parse(kwargs):
    data = {}
    DCType = kwargs.get('type')
    data['pos'] = kwargs.get('align', 'left')
    data['size'] = kwargs.get('size', 'large')
    if (DCType.upper() == 'NOTE'):
        data['documentId'] = kwargs.get('documentid')
        data['noteId'] = kwargs.get('noteid')
        return render_to_string(
            'shortcodes/documentCloud/documentCloudNote.html', data)
