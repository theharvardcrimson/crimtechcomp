from __future__ import absolute_import

import os

from django.conf import settings
from django.http import Http404

import requests
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crimsononline.settings')


# Celery stuff
app = Celery('crimsononline')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task()
def get_keywords_task(art_pk):
    from crimsononline.content.recommended_articles import get_keywords
    from crimsononline.content.models import Article
    article = Article.objects.get(pk=art_pk)
    get_keywords(article)
    return article


@app.task()
def generate_rec_articles_task(art_pk):
    from crimsononline.content.recommended_articles import (
        generate_rec_articles)
    from crimsononline.content.models import Article
    article = Article.objects.get(pk=art_pk)
    generate_rec_articles(article)


@app.task()
def cache_homepage():
    """Render and cache the homepage."""
    from django.core.cache import cache
    from crimsononline.content.models import Index

    try:
        index = Index.objects.get()
    except Index.DoesNotExist, Index.MultipleObjectsReturned:
        raise Http404

    data = {}

    homepage = index.layout.render_to_string(data)
    cache.set('homepage', homepage, settings.CACHE_EONS)

    return homepage


def top_articles(section):
    """Return a queryset of prioritized articles from section"""
    from django.db.models import Q
    from crimsononline.content.models import Article

    if not isinstance(section, list):
        section = [section]

    q = Q()
    for s in section:
        if isinstance(s, basestring):
            q |= Q(section__name=s)
        else:
            q |= Q(section=s)

    stories = Article.objects.prioritized(50).filter(q)
    if not stories:
        stories = Article.objects.prioritized(150).filter(q)

    return stories


@app.task()
def purge_facebook(url):
    payload = {'id': url, 'scrape': True}
    requests.post('https://graph.facebook.com', data=payload)
