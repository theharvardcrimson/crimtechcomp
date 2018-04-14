from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from BeautifulSoup import BeautifulSoup

from crimsononline.content.generators import top_articles
from crimsononline.content.models import (
    Article, Content, Contributor, Section, Tag)
from crimsononline.shortcodes import parser

title = u'The Harvard Crimson | '
num_items = 25


# authors
class AuthorFeed(Feed):
    # author info for header
    def get_object(self, request, pk):
        return get_object_or_404(Contributor, pk=pk)

    # author's rss feed title
    def title(self, obj):
        if not obj:
            raise FeedDoesNotExist
        # The Harvard Crimson | Writer | Alexander H. Patel
        return title + u'Writer | ' + unicode(obj)

    # link to author page
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()  # called by default, but just to check

    # description of author's rss
    def description(self, obj):
        return u'Content by {0}'.format(unicode(obj))

    # author's content for feed items
    # returns last num_items content produced by author
    def items(self, obj):
        return Article.objects.filter(contributors=obj) \
                              .order_by('-modified_on')[:num_items]

    # title of any given article produced by author
    def item_title(self, item):
        return item.title

    # same as above, but description
    def item_description(self, item):
        # Returns teaser text or before-jump text; whichever is present
        return item.snippet

    # same as above, but with link to content
    def item_link(self, item):
        # defaults to get_abs_url, but it's a django backup
        return item.get_absolute_url()


# sections
class SectionFeed(Feed):
    # section info for header
    def get_object(self, request, section):
        # the section objects have capitalized names
        section = section.capitalize()
        return get_object_or_404(Section, name=section)

    def title(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return title + u'Section | ' + unicode(obj.name)

    def description(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return u'Content for the {0} section'.format(unicode(obj.name))

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        # It should default to get_abs_url, but I get a null pointer
        # when it does
        return obj.get_absolute_url()

    # section content for rss items
    # item_link defaults to get_absolute_url

    # get first num_items articles for section
    def items(self, obj):
        items = top_articles(obj)
        return items[:num_items]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.snippet

    def item_link(self, item):
        return item.get_absolute_url()


class FullSectionFeed(SectionFeed):
    def item_description(self, item):
        soup = BeautifulSoup(item.text.replace('<p>&nbsp;</p>', ''))
        return parser.parse(soup.renderContents())


# tags
class TagFeed(Feed):
    # tag info for header
    def get_object(self, request, tagname):
        return get_object_or_404(Tag, text=tagname)

    def title(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return title + unicode(obj)

    def description(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return 'Content for tag: \"{0}\"'.format(unicode(obj))

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    # tag's content for feed items
    def items(self, obj):
        items = Content.objects.filter(tags=obj).order_by('-issue__issue_date')
        return items[:num_items]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return ''  # no description field for content - figure out later

    def item_link(self, item):
        return item.get_absolute_url()


# # featured articles
class FeatureFeed(TagFeed):
    # feature info for header
    def get_object(self, request):
        return get_object_or_404(Tag, text='Features')

    def title(self, obj):
        return title + 'Featured Articles'

    def description(self, obj):
        return 'Featured Articles from The Harvard Crimson'

    def link(self, obj):
        return reverse('content.section.features')

    def items(self, obj):
        items = Content.sobjects.recent \
                                .filter(tags__text='Features')
        return items[:num_items]

    def item_description(self, item):
        return item.description
