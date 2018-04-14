Content
=======

Article
-------

Non serial text content

.. code-block:: python

    # create some articles
    >>> c = Contributor.objects.create(first_name='Kristina',
    ...     last_name='Moore')
    >>> t = Tag.objects.create(text='tagg')
    >>> i = Issue.get_current()
    >>> s = Section.objects.create(name='movies')
    >>> a1 = Article.objects.create(headline='abc', text='abcdefg',
    ...     issue=i, section=s)
    >>> a2 = Article.objects.create(headline='head line',
    ...     text='omg. lolz.', issue=i, section=s, proofer=c, sne=c)
    # teasers
    >>> str(a2.long_teaser)
    'omg. lolz.'

byline_type
^^^^^^^^^^^
This indicates whether the writers are `Crimson Staff Writers` or `Contributing Writers`

text
^^^^
Article text.

page
^^^^
Page in the print edition

layout_instance
^^^^^^^^^^^^^^^
The layout of this article.

rel_content
^^^^^^^^^^^
Related Content. These are articles that editors manually assign to new articles.

rec_articles
^^^^^^^^^^^^
Recommended Articles. These are articles that are automatically found based on content similarity.

parent_topic
^^^^^^^^^^^^
The `TopicPage` that this article belongs to. See TopicPages for more detail

tagline
^^^^^^^
Indicates whether or not to automatically generated the teaser text for an article.


rel_admin_content
^^^^^^^^^^^^^^^^^
Returns all content relations related to this article. This includes other articles, images, etc.

rec_articles_admin
^^^^^^^^^^^^^^^^^^
Returns a semicolon-separated list of all primary keys of recommended articles.

has_jump
^^^^^^^^
True if there is a `<!--more-->` line in the text.

text_before_jump
^^^^^^^^^^^^^^^^
True if there is text before the `<!--more-->` line.

snippet
^^^^^^^
Returns teaser text or before-jump text; whichever is present.

groupless_headline
^^^^^^^^^^^^^^^^^^
Removes the title of the group from the title of the article. E.g. `Steven's column: Random title` becomes `Random title`

save
^^^^
Override the default save behavior. If a published article was changed, create a new `Correction` object from the change, and queues up recommended articles.

delete
^^^^^^
Override the default delete behavior. Clears all `related content` relations before deleting this object.

long_teaser
^^^^^^^^^^^
Returns the first 50 words of the title (strips HTML).

main_rel_content
^^^^^^^^^^^^^^^^
Returns the first related content object that is not an article. This is usually an image or anything that can be treated as an image.

main_rel_content_is_shortcoded
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Returns True if `main_rel_content` is shortcoded.

rel_not_shortcoded
^^^^^^^^^^^^^^^^^^
Gives you the related content minus all content that has been shortcoded in.

rel_shortcoded
^^^^^^^^^^^^^^
Returns a list of all shortcoded content ids, regardless of whether or not it is traditionally related with an `ArticleContentRelation`.

extract_shortcoded_content
^^^^^^^^^^^^^^^^^^^^^^^^^^
Searches the text for shortcodes and adds them to the list of shortcoes.
