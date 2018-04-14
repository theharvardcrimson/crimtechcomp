from django import template

from crimsononline.content.models import Article, Section, Tag

register = template.Library()

editors_choice_tag = Tag.objects.get(text="Editors' Choice")


@register.inclusion_tag('templatetag/editorschoice.html')
def editors_choice(section=None, title=None, num=5):
    if not title:
        title = "%s Editors' Choice" % section.capitalize()

    articles = Article.objects.filter(tags=editors_choice_tag)
    if section:
        articles = articles.filter(section=Section.cached(section))

    return {
        'title': title,
        'articles': articles.order_by('-created_on')[:num]
    }
