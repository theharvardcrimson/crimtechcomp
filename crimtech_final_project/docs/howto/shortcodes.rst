Shortcodes documentation
========================

Shortcodes are little code snippets that are used to insert image, pdf, tweet or a video in an article. The documentation on how to use a shortcode can be found `here
<https://docs.google.com/document/d/1HW4nnqLzkEoh1gN4AfnYgpYDLw8wPV1B3GaAK7fhASA/>`_.

Consider this piece of code inside an article::

	{pullquote text = "Hello World!" align = right}

This shortcode takes in the string ``Hello World!`` and renders a quote on the article page.

Writing a shortcode is very easy. A shortcode is made of three parts.

- The parser
- The view
- CSS

Beginning with a shortcode
--------------------------
The shortcode web app at ``crimsononline/shortcodes`` handles all shortcode.

Every shortcode has a parser and a view. The parsers are located in ``crimsononline/shortcodes/parsers/``. The views are located in ``crimsononline/shortcodes/templates/shortcodes/``.

To create a shortcode, start by creating a parser ``yourshortcode.py`` in the parsers directory and a view ``yourshortcode.html`` in the views directory. For now, you may copy the content of ``pullquote.py`` and ``pullquote.html`` to avoid coding from scratch. The pullquote is one of the simplest shortcode we have and provides the necessary bare structure to your new shortcode.

The parser
----------

A parser decodes the short-code string and feeds in values to the view which will then render the image or a tweet on a page.

Consider this line in ``pullquote.py``::

	data['text'] = kwargs.get('text')

*data* is a dictionary and this line of code takes in what is defined as *text* in the shortcode and adds it to the dictionary.

Similarly, this line of code::

	data['pos'] = kwargs.get('align', 'left')

takes in any desired alignment. If the editor hasn't specified any alignment, it choosed left by default.

**Example**
	To do something more complicated, say get an image ID and print the title of the image.::

		sc_id = kwargs.get('id')
		data = {}
		try:
			data['image'] = Image.objects.get(pk=sc_id)
		except:
			if settings.TEMPLATE_DEBUG:
				raise Exception('Image with id ' + sc_id + ' not found or unpublished')
			else:
				return ''
		data['title'] = data['image'].title
	This piece of code takes in an image ID, looks up the image in the database (which appropriate error handling). If the image exists, it then proceeds to get the title of that image.


Now, having absorbed the relevant values to the dictionary, we can pass the dictionary to the corresponding view/template to render it.::

	 return render_to_string('shortcodes/pullquote.html', data)


The view
----------

The view is a html file which renders the data passed from parsers onto the article page. Again, it is helpful to inherit the base structure  from ``pullquote.html``.

Every view needs the following base structure::

	{% extends "shortcodes/_base.html" %}

	{% block content %}
	...
	{% endblock %}

The relevant content goes inside the *block*. Consider the example from ``pullquote.html``.::

	<blockquote{% if font %} style="font-family:{{ font }}"{% endif %}>
		{{ text }}
	</blockquote>

What is does is pretty straightforward. It simply renders ``data['text']`` along with any font styles if any defined.

For something more complicated, refer to the image view ``image.html``.


CSS
----
All shortcodes CSS are defined inside ``crimsononline/static/css/shortcodes/``. For your shortcode, create a file inside this directory with the name ``_yourshortcode.scss``.

Add relevant CSS to this file.

And finally, import this newly created CSS in ``crimsononline/static/css/shortcodes.scss``::

	@import 'shortcodes/yourshortcode';

Notice that the underscore is not necessary in the import statement.

Now, try creating an article with your shortcode from admin. Once you are done, go ahead and push the code.
