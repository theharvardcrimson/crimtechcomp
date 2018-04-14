from redactor.widgets import RedactorEditor

DEFAULT_REDACTOR_OPTIONS = {
    'buttons': [
        'formatting', 'bold', 'italic', 'deleted',
        'unorderedlist', 'orderedlist', 'link', 'html',
    ],
    'convertUrlLinks': False,
    'convertVideoLinks': False,
    'convertImageLinks': False,
    'formatting': ['p', 'h2', 'h3', 'h4'],
    'maxHeight': 550,
    'tabKey': False,
    'toolbarFixed': False,
    'plugins': ['pagebreak', 'shortcodes'],
    'replaceTags': [
        ['strike', 'del'],
        ['i', 'em'],
        ['b', 'strong'],
    ]
}

SAFE_REDACTOR_OPTIONS = {
    'allowedTags': [
        'a', 'br', 'del', 'em', 'h2', 'h3', 'h4', 'hr', 'li' 'ol', 'p',
        'span', 'strong', 'ul'
    ]
}


class UnsafeWYSIWYGEditor(RedactorEditor):
    """A WYSIWYGEditor for power users that allows most HTML markup"""

    def __init__(self, editor_options=None):
        merged_options = DEFAULT_REDACTOR_OPTIONS.copy()
        if editor_options:
            merged_options.update(editor_options)
        return super(UnsafeWYSIWYGEditor, self).__init__(
            allow_file_upload=False,
            allow_image_upload=False,
            redactor_options=merged_options
        )

    class Media:
        css = {
            'all': (
                'texteditors/redactor/crimson.css',
                'redactor/plugins/pagebreak.css',
            )
        }


class WYSIWYGEditor(UnsafeWYSIWYGEditor):
    """A WYSIWYGEditor that prevents mishaps by disallowing most HTML markup"""

    def __init__(self, editor_options=None):
        merged_options = SAFE_REDACTOR_OPTIONS.copy()
        if editor_options:
            merged_options.update(editor_options)
        return super(WYSIWYGEditor, self).__init__(merged_options)
