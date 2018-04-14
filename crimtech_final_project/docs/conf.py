extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'crimsononline'
copyright = u'2015, The Harvard Crimson'
author = u'The Harvard Crimson'

version = '0.0.1'
release = '0.0.1'

language = None

exclude_patterns = ['_build']

pygments_style = 'sphinx'

todo_include_todos = True

html_theme = 'alabaster'

html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'crimsononlinedoc'

latex_documents = [
    (master_doc, 'crimsononline.tex', u'crimsononline Documentation',
     u'The Harvard Crimson', 'manual'),
]

man_pages = [
    (master_doc, 'crimsononline', u'crimsononline Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'crimsononline', u'crimsononline Documentation',
     author, 'crimsononline', 'One line description of project.',
     'Miscellaneous'),
]
