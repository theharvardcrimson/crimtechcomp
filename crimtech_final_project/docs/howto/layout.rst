Creating a  Layout
=====================

All article templates are stored in ``placeholders/templates``. To create a new template layout, create a HTML file ``yourlayout.html`` in this folder. You may use ``rotc.html`` for reference.

``rotc.html`` then links to ``rotc.css`` for its design. Change this reference to your new css ``yourlayout.css``::

	 <link rel="stylesheet" type="text/x-scss" media="all"
	 href="{{ STATIC_URL }}css/yourlayout.scss">

Layout doesnot have an admin interface. For the local machine, it can be created through shell plus.::

	 $ ./vagrant_manage.sh shell_plus

Create a new Layout object.::

	 > newLayout = Layout()
	 > newLayout.name = 'Your Layout Title'
	 > newLayout.template_path = 'placeholders/yourlayout.html'
	 > newLayout.article_template = True
	 > newLayout.gallery_template = False
	 > newLayout.save()

Now, your new Layout is visible in Article Admin form.
