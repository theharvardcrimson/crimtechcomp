from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Count
from django.template.loader import render_to_string

from crimsononline.common.caching import funcache
from crimsononline.content.models import (
    Article, Content, ContentGroup, TopicPage, Video)

register = template.Library()


class FlyByNode(template.Node):
    """
    Generates a flyby widget.
    """
    def render(self, context):
        flyby_preview = cache.get('flyby_preview')
        types = [ContentType.objects.get_for_model(m)
                 for m in [Article, TopicPage]]
        if flyby_preview is None:
            self.posts = Content.sobjects \
                                .recent \
                                .select_subclasses(Article, TopicPage) \
                                .filter(content_type__in=types) \
                                .filter(tags__text='Flyby Front') \
                                .exclude(tags__text='Flyby Front Feature')[:3]
            try:
                self.feature = Content \
                                .sobjects \
                                .recent \
                                .select_subclasses(Article, TopicPage) \
                                .filter(content_type__in=types) \
                                .filter(tags__text='Flyby Front Feature')[0]

            except IndexError:
                self.feature = self.posts[2]

            flyby_preview = render_to_string(
                'templatetag/flyby_preview.html',
                {'posts': self.posts, 'feature': self.feature})
            cache.set('flyby_preview', flyby_preview, settings.CACHE_STANDARD)
            return flyby_preview
        else:
            return flyby_preview


@funcache(settings.CACHE_STANDARD, 'flyby_preview')
def do_flyby(parser, token, nopreview=False):
    return FlyByNode()


register.tag('flyby_preview', do_flyby)


class BlogNode(template.Node):
    """
    Generates a blog widget thing that doesn't have the Flyby logo.
    TODO: Generalize this so that it works for contentgroups that are
    not the sports blog.
    """
    def render(self, context):
        sb = ContentGroup.objects.get(name='The Back Page')

        self.posts = Article.objects \
                            .recent \
                            .filter(group=sb) \
                            .annotate(num_related=Count('rel_content')) \
                            .filter(num_related__gt=0)[:4]

        return render_to_string(
            'templatetag/blog_preview.html',
            {'posts': self.posts})


@funcache(settings.CACHE_STANDARD, 'blog_preview')
def do_blog(parser, token, nopreview=False):
    return BlogNode()


register.tag('blog_preview', do_blog)


class MediaBoxNode(template.Node):
    def render(self, context):
        videos = Video.objects.prioritized(60)  # TODO: why 60?!
        return render_to_string(
            'templatetag/media_box.html', {'videos': videos})


@funcache(settings.CACHE_STANDARD, 'media_box')
def do_media_box(parser, token, nopreview=False):
    return MediaBoxNode()


register.tag('media_box', do_media_box)
