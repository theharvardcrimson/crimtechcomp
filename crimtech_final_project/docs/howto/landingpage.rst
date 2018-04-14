Creating a  Landing Page
=====================

Landing Page templates can be stored in a variety of places, but typically they should be stored in ``content/templates/models/topicpage``. To create a new template layout, create a HTML file ``yourlayout.html`` in this folder. You may use ``commencement-2017/landing.html`` for reference.

Please reference ``commencement-2017/_base.html`` on how css and js can be piped into a landing page.
Please reference ``content/templates/FM-Year-in-Review-2016/fmyearinreview2016.html`` for a landing page that extends the standard base.

This html is converted into a Layout object. This Layout object has placeholders which are filled by a Layout Instance object, which will render the pure html for the landing page. Layout Instance objects can be linked to Topic Page objects, which allow a landing page to get a special url (ie. thecrimson.com/topic/commencement-2017/) and allow it to a preview to appear on the homepage or section landing page similar to how an article appears.


Layout does not have an admin interface. For the local machine, it can be created through shell plus. ::

	 $ ./vagrant_manage.sh shell_plus

Create a new Layout object. ::

	 > newLayout = Layout()
	 > newLayout.name = 'Your Layout Title'
	 > newLayout.template_path = 'path/to/yourlayout.html'
	 > newLayout.article_template = False
	 > newLayout.gallery_template = False
	 > newLayout.save()

Now,
your new Layout is visible in Article Admin form. If you edit the placeholders or any django piping (not html) within ``yourlayout.html`` you will have to relanch shell plus and resave the Layout. ::
   > layoutToResave = Layout.objects.get(name = 'Your Layout Title')
   > layoutToResave.save()

Layout Instance and Topic Page have an admin interface.

If a topic page is needed, first create a Topic Page with the relevant information. Saving the Topic Page will automatically create a linked Layout Instance.

The linked Layout Instance can be accessed through the link on the specific Topic Page or the general Layout Instance admin page. Edit the Layout Instance as wanted.

The specific topic page can be Preview-ed before publishing.
