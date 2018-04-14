from django import template

from crimsononline.content.models import MostReadArticles

register = template.Library()


def most_read(context, specifier):
    try:
        context['mostreadarticles'] = (MostReadArticles.objects
                                       .filter(key=specifier)
                                       .order_by('-create_date')[0]
                                       .articles)
    except IndexError, MostReadArticles.DoesNotExist:
        pass

    return context


@register.inclusion_tag('templatetag/mostreadarticles.html',
                        takes_context=True)
def most_read_articles(context):
    return most_read(context, 'content')


@register.inclusion_tag('templatetag/mostreadadmissions.html',
                        takes_context=True)
def most_read_admissions(context):
    return most_read(context, 'admissions')


@register.inclusion_tag('templatetag/mostreadflyby.html',
                        takes_context=True)
def most_read_flyby(context):
    return most_read(context, 'flyby')


@register.inclusion_tag('templatetag/relatedarticles.html',
                        takes_context=True)
def related_articles(context):
    return context


@register.inclusion_tag('templatetag/recommended_articles.html',
                        takes_context=True)
def recommended_articles(context):
    return context
