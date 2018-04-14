from django import template
from django.template.loader import render_to_string

from crimsononline.content.models import Article, Section

register = template.Library()


class ArtsBlogNode(template.Node):
    """
    Generates a arts blog widget.
    """
    def render(self, context):
        arts = Section.cached('arts')
        try:
            self.feature = Article.objects \
                                .recent \
                                .filter(tags__text='Arts Blog Front Feature') \
                                .filter(section=arts)[0]
        except IndexError:
            self.feature = Article.objects \
                                  .recent \
                                  .filter(section=arts) \
                                  .filter(tags__text='Arts Blog')[0]

        self.posts = Article.objects \
                            .recent \
                            .filter(section=arts) \
                            .filter(tags__text='Arts Blog') \
                            .exclude(pk=self.feature.pk)[:2]

        return render_to_string(
            'templatetag/arts_blog_preview.html',
            {'posts': self.posts, 'feature': self.feature}
        )


def do_arts_blog(parser, token, nopreview=False):
    return ArtsBlogNode()


register.tag('arts_blog_preview', do_arts_blog)
