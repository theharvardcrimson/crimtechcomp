import hashlib
import json
import logging
import random
import re
import string
from datetime import date, datetime, timedelta

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache as _djcache
from django.db import connection
from django.db.models import Max, Q, Sum
from django.http import (
    Http404, HttpResponse, HttpResponseRedirect, JsonResponse)
from django.shortcuts import (
    get_list_or_404, get_object_or_404, redirect, render, render_to_response)
from django.template import TemplateDoesNotExist, loader
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page
from django.views.generic import View

import PIL
import requests
from templatetags.content_filters import byline, get_image_obj, img_url

from crimsononline.common.caching import funcache as cache
from crimsononline.common.utils.lists import first_or_none
from crimsononline.common.utils.paginate import paginate
from crimsononline.common.utils.urlnames import fullname, urlname
from crimsononline.common.utils.watermark import watermark
from crimsononline.content.generators import cache_homepage, top_articles
from crimsononline.content.models import (
    Article, Content, ContentGroup, Contributor, FeaturePackage, Gallery,
    Image, Issue, PackageSectionContentRelation, Score, Section, Tag,
    TopicPage, Video)
from crimsononline.local_settings import ISSUU_API_KEY, ISSUU_API_SECRET
from crimsononline.placeholders.models import LayoutInstance

logger = logging.getLogger(__name__)


@cache(settings.CACHE_STANDARD, 'sitemap')
def sitemap(request, year=None, issue=None):
    if year is None:
        oldest = Article.objects.order_by(
            'issue__issue_date')[0].issue.issue_date.year
        newest = Article.objects.order_by(
            '-issue__issue_date')[0].issue.issue_date.year
        years = range(newest, oldest - 1, -1)
        return render_to_response(
            'sitemap/sitemap_base.html',
            {'years': years},
            context_instance=RequestContext(request))
    elif year is not None and issue is None:
        issues = Issue.objects.filter(issue_date__year=year).order_by(
            'issue_date')
        return render_to_response(
            'sitemap/sitemap_issues.html',
            {'year': year, 'issues': issues},
            context_instance=RequestContext(request))
    elif issue is not None:
        try:
            issue = Issue.objects.get(pk=issue)
            ars = Article.objects.filter(issue=issue)
            return render_to_response(
                'sitemap/sitemap_articles.html',
                {'articles': ars, 'issue': issue},
                context_instance=RequestContext(request))
        except:
            raise Http404


@cache(settings.CACHE_STANDARD, 'sitemap-contributors')
def sitemap_contributors(request, page=None):
    contributors_per_page = 100

    if page is not None:
        page = int(page)
        first = contributors_per_page * (page - 1)
        last = contributors_per_page * page - 1
        contribs = Contributor.objects.all()[first:last]
        return render_to_response(
            'sitemap/sitemap_contributors_page.html',
            {'contribs': contribs, 'page': page},
            context_instance=RequestContext(request))
    else:
        num_contributors = len(Contributor.objects.all())
        pages = range(num_contributors / contributors_per_page + 2)[1:]

        return render_to_response(
            'sitemap/sitemap_contributors_base.html',
            {'pages': pages},
            context_instance=RequestContext(request))


def index(request):
    """Show the view for the front page."""
    homepage = _djcache.get('homepage')
    if homepage is None:
        return HttpResponse(cache_homepage())
    else:
        return HttpResponse(homepage)


REMOVE_P_RE = re.compile(r'page/\d+/$')


@cache_page(settings.CACHE_LONG)
def writer(request, pk, f_name, m_name, l_name, page=1, sections=None,
           types=None):
    """Show the view for a specific writer."""

    # Validate the URL (we don't want /writer/281/Balls_Q_McTitties to
    # be valid)
    w = get_object_or_404(Contributor, pk=pk)
    if (w.first_name, w.middle_name, w.last_name) != (f_name, m_name, l_name):
        return HttpResponseRedirect(w.get_absolute_url())

    filtered = filter_helper(
        request, w.content.all().order_by('-issue__issue_date'),
        sections, types, w.get_absolute_url()
    )

    if request.method == 'POST':
        try:
            content = paginate(filtered.pop('content'), page, 15).get('content')
            articles = [article._render('preview-list') for article in content]
            return JsonResponse({'articles': articles})
        except Http404:
            return JsonResponse({'articles': []})
    else:
        page = 1  # GET requests will always get the first page of results
        url_base = '/writer/%s/%s_%s_%s' % (pk, f_name, m_name, l_name)
        w.number_of_articles = Article.objects.filter(contributors=w).count()

        objs = Content.objects.filter(contributors=w)
        latest = objs.aggregate(Max('issue__issue_date'))
        w.last_update = latest['issue__issue_date__max']

        context = paginate(filtered.pop('content'), page, 15)
        context.update({
            'writer': w,
            'url_base': url_base,
            'rss_url': w.rss_url,
            'writer_byline': mark_safe(w.get_tagline())
        })

        if w.image:
            context['img_url'] = w.pic_display_url((150, 150, 150, 150))

        if 'ajax' in request.GET:
            data = {
                'content_list': render_to_string(
                    'ajax/content_list_page.html', context
                ),
                'content_filters': render_to_string(
                    'ajax/content_list_filters.html', context
                )
            }
            return JsonResponse(data)

        return render(request, 'writer.html', context)


@cache_page(settings.CACHE_LONG)
def tag(request, tagname, page=1, sections=None, types=None):
    """Show the view for a single tag"""
    fulltag = fullname(Tag, 'text', tagname)

    t = get_object_or_404(Tag, text=fulltag)
    try:
        t2 = Tag.objects.get(text__iexact=tagname)
    except:
        t2 = None

    absurl = t.get_absolute_url()
    if (urlname(t.text) != tagname):
        return HttpResponseRedirect(absurl)

    if t2 is not None:
        a = Content.objects.filter(tags__in=(t, t2)).order_by(
            '-issue__issue_date')
    else:
        a = Content.objects.filter(tags=t).order_by('-issue__issue_date')

    if sections:
        secs = get_list_or_404(Section, name__in=sections.split(','))
        a = a.filter(section__in=secs)
    if types:
        typesl = get_list_or_404(ContentType, model__in=types.split(','))
        a = a.filter(content_type__in=typesl)

    data = paginate(a, page, 15)
    data['tagname'] = t.text
    data['url_base'] = absurl
    data['urltagname'] = tagname
    data['rss_url'] = t.rss_url
    if sections:
        # NEEDS A BETTER WAY TO AVOID REFERENCING URL!!!
        data['url_base'] += '/sections/%s' % sections
    if types:
        # NEEDS A BETTER WAY TO AVOID REFERENCING URL!!!
        data['url_base'] += '/types/%s' % types
    data['sectionlist'] = [
        obj['name'] for obj in Section.objects.values('name')
        if obj['name'] != ''
    ]
    data['typelist'] = [type.name.title() for type in Content.types()]

    if sections:
        data['secs'] = [sec.name for sec in secs]
    if types:
        data['types'] = [type.name.title() for type in typesl]

    if 'ajax' in request.GET:
        return render_to_response('ajax/tag.html', data)
    else:
        return render(request, 'tag.html', data)


@cache(settings.CACHE_LONG)
def get_tag_top_contribs(pk):
    # top writers (contributors that have the most content with this tag)
    cursor = connection.cursor()
    # TODO: should actually do this with sqlite3 replacement, not python
    cursor.execute("""SELECT
            content_contributors.contributor_id,
            count(content.id) AS objcount
        FROM
            content_content AS content,
            content_content_contributors AS content_contributors,
            content_content_tags AS content_tags
        WHERE
            content_contributors.content_id = content.id AND
            content_tags.content_id = content.id AND
            content.id NOT IN (SELECT content_ptr_id FROM content_image) AND
            content_tags.tag_id = %i AND
            content.pub_status = 1
        GROUP BY content_contributors.contributor_id
        ORDER BY objcount DESC
        LIMIT 5
    """ % pk)
    rows = [r for r in cursor.fetchall() if r[1] > 0]
    writers = Contributor.objects.filter(pk__in=[r[0] for r in rows])
    contrib_count = dict(rows)
    for w in writers:
        w.c_count = contrib_count[w.pk]
        w.rece = w.content.recent[:1][0].issue.issue_date
    writers = list(writers)
    writers.sort(lambda x, y: cmp(y.c_count, x.c_count))
    return writers


@cache(settings.CACHE_LONG)
def get_related_tags(pk):
    # related tags (tags with most shared content)
    #  select the tags for which there are the most objects that have both
    #  this tag and that tag within some timeframe
    cursor = connection.cursor()
    cursor.execute("""SELECT cgt2.tag_id,
        count(cgt2.content_id) AS o_count
        FROM content_content_tags AS cgt1
        JOIN content_content_tags AS cgt2
        ON cgt1.content_id=cgt2.content_id
        WHERE cgt1.tag_id = %(pk)i AND cgt2.tag_id != %(pk)i
        GROUP BY cgt2.tag_id ORDER BY o_count DESC LIMIT 15;""" % {'pk': pk})
    rows = cursor.fetchall()
    tags = Tag.objects.filter(pk__in=[r[0] for r in rows])
    tags_count = dict(rows)
    for t in tags:
        t.content_count = tags_count[t.pk]
    tags = list(tags)
    tags.sort(lambda x, y: cmp(y.content_count, x.content_count))
    return tags


@cache_page(settings.CACHE_STANDARD)
def topic_page(request, slug_path):
    try:
        t = TopicPage.objects.get(slug_path=slug_path)
    except (TopicPage.DoesNotExist, ValueError):
        raise Http404

    data = {'topic': t, 'nav': t.section.name.lower()}
    return t.layout_instance.render(request, data)


@cache_page(settings.CACHE_SHORT)
def section_news(request):
    """Show the view for the news section page."""

    nav = 'news'
    ad_zone = 'content'
    section = Section.cached(nav)
    stories = top_articles(section)[:25]

    rss_url = section.rss_url  # url for section's rss feed

    today = datetime.today()
    lastweek = today - timedelta(7)
    lastmonth = today - timedelta(120)

    photos = []
    for story in stories:
        if story.main_rel_content:
            photos.append(story)

    featured = Article.objects.filter(tags__text='news front feature') \
        .filter(rel_content__isnull=False) \
        .order_by('-created_on')

    return section.layout.render(request, locals())


# Helper method for section_opinion and opinion_postcards
def postcard_has_loc(article):
        postcard_re = re.compile(ur'([^\u2010-\u2015\-<>]+)[\u2010-\u2015\-]')
        try:
            loc = postcard_re.findall(article.text)[0]
            if len(loc) > 50:
                return False
            return True
        except IndexError:
            return False


@cache_page(settings.CACHE_SHORT)
def section_opinion(request):
    """Show the view for the opinion section page."""

    nav = 'lol what does this do'#'opinion'
    section = Section.cached(nav)
    ad_zone = 'content'
    columns = ContentGroup.objects.filter(
        section=section, active=True,
        type='column').annotate(
        recent=Max('content__issue__issue_date')).order_by('-recent')

    rss_url = section.rss_url  # url for section's rss feed

    # Get postcard info
    tag = 'Summer Postcards '
    postcard_articles_all = Article.objects.filter(tags__text__startswith=tag)\
        .filter(~Q(title__startswith='Crimson Summer Postcards '))\
        .filter(~Q(title__contains='Postcards This Week '))\
        .filter(~Q(
            title__startswith='This Summer, Crimson Editors Are Traveling'))\
        .order_by('-created_on').distinct()

    postcard = None
    for c in postcard_articles_all:
        if get_image_obj(c) and postcard_has_loc(c):
            postcard = c
            break

    postcard = None
    # hey Richard, I'll implement the iterable here, don't touch!!

    loc = re.findall(
        ur'([^\u2010-\u2015\-<>]+)[\u2010-\u2015\-]', postcard.text)[0]
    country = None
    try:
        country = loc.split(',')[1].strip().title()
    except IndexError:
        pass

    card = {
        'article': postcard,
        'city': loc.split(',')[0].strip().title(),
        'country': country,
        'postmark': 'postmark1',
        'class': 'postcard-type2'
    }

    return section.layout.render(request, locals())


@cache_page(settings.CACHE_SHORT)
def opinion_postcards(request, year=None):
    """ Display the summer postcards page """
    postcard_re = re.compile(ur'([^\u2010-\u2015\-<>]+)[\u2010-\u2015\-]')
    first_year = 2011

    def map_helper(article):
        loc = postcard_re.findall(article.text)[0]
        country = ''
        try:
            country = loc.split(',')[1].strip().title()
        except IndexError:
            pass

        return {
            'city': loc.split(',')[0].strip().title(),
            'country': country,
            'article': article,
            'postmark': 'postmark' + str(random.randint(1, 2)),
            'class': 'postcard-type' + str(random.randint(1, 2))
        }

    tag = 'Summer Postcards '
    postcard_articles_all = Article.objects.filter(tags__text__startswith=tag)\
        .filter(~Q(title__startswith='Crimson Summer Postcards '))\
        .filter(~Q(title__contains='Postcards This Week '))\
        .filter(~Q(
            title__startswith='This Summer, Crimson Editors Are Traveling'))\
        .order_by('-created_on').distinct()

    # Figure out year
    most_recent = postcard_articles_all[0].created_on.year
    if year is None:
        year = most_recent

    else:
        year = int(year)

    postcard_articles = postcard_articles_all.filter(created_on__year=year)

    if not postcard_articles:
        raise Http404

    page = 1
    if 'p' in request.GET:
        try:
            page = int(request.GET['p'])
            if page <= 0:
                return redirect('/section/opinion/postcards')
        except ValueError:
            return redirect('/section/opinion/postcards')

    latest = postcard_articles[0].created_on
    delta = timedelta(days=7)
    postcard_articles_page = postcard_articles\
        .filter(created_on__range=[latest - page * delta,
                latest - (page - 1) * delta])

    # Ensure cards with images go to the front of the list
    with_img = []
    without_img = []
    for a in postcard_articles_page:
        if not postcard_has_loc(a):
            pass
        elif a.main_rel_content:
            with_img.append(a)
        else:
            without_img.append(a)

    postcard_articles_page = with_img + without_img

    if len(postcard_articles_page) == 0:
        return redirect('/section/opinion/postcards')

    last_page = 1
    while postcard_articles.filter(created_on__lt=latest - last_page * delta):
        last_page += 1

    # p = pagination information
    p = {}
    p['page'] = page
    p['next_page_number'] = page + 1
    p['previous_page_number'] = page - 1
    p['last'] = last_page
    p['has_prev'] = p['previous_page_number'] >= 1
    p['has_next'] = p['page'] < last_page
    p['prev_year'] = year + 1
    p['next_year'] = year - 1
    p['has_prev_year'] = False
    p['has_next_year'] = False

    if p['prev_year'] <= most_recent:
        p['has_prev_year'] = True

    if p['next_year'] >= first_year:
        p['has_next_year'] = True

    # The ratio of the heights of a regular article title/teaser and a
    # postcard is approximately 1:2 - seems to work well enough in most
    # cases
    num_cards = int(round(0.5 * len(postcard_articles_page)))
    postcards = map(map_helper, postcard_articles_page[:num_cards])

    other_postcards = postcard_articles_page[num_cards:]

    data = {
        'year': year,
        'postcards': postcards,
        'other_postcards': other_postcards,
        'p': p
    }
    return render(request, 'sections/opinion-postcards.html', data)


class FMView(View):
    section_name = 'magazine'

    def get(self, request):
        section = Section.cached(self.section_name)
        return section.layout.render(request, {
            'ad_zone': 'content',
            'section': section
        })

    def dispatch(self, *args, **kwargs):
        return cache_page(settings.CACHE_SHORT)(super(FMView, self).dispatch)(
            *args, **kwargs)


def fm_paginate(request):
    if request.method == 'POST':
        fields = ['section', 'offset', 'count']
        missing = ["'" + x + "'" for x in fields if x not in request.POST]
        if missing:
            return JsonResponse(
                data={'error': 'missing ' + ' and '.join(missing)},
                status=400
            )

        section_tags = {
            u'': [],
            u'issues': ['Scrutiny'],
            u'levity': ['Levity', 'A Little Levity'],
            u'around-town': ['Around Town'],
            u'introspection': ['Introspection'],
            u'conversations': ['Conversations'],
            u'retrospection': ['Retrospection'],
            u'the-scoop': ['The Scoop']
        }

        section = request.POST['section']
        if section not in section_tags:
            return JsonResponse(
                data={'error': 'invalid section: ' + section},
                status=400
            )

        offset = request.POST['offset']
        if not offset.isdigit() or int(offset) < 0:
            return JsonResponse(
                data={'error': 'offset must be a non-negative integer'},
                status=400
            )

        count = request.POST['count']
        if not count.isdigit() or int(count) < 0:
            return JsonResponse(
                data={'error': 'count must be a non-negative integer'},
                status=400
            )

        if int(count) > 20:
            return JsonResponse(
                data={'error': 'cannot request more than 20 articles'},
                status=400
            )

        fm = Section.cached('magazine')
        tags = section_tags[section]

        items = Article.objects.filter(section=fm).order_by('-created_on')
        if tags:
            items = items.filter(tags__text__in=tags)

        results = []
        for article in items[int(offset):int(offset) + int(count)]:
            subsection = article.fm_subsection()
            results.append({
                'url': article.get_absolute_url(),
                'image': img_url(get_image_obj(article), [360, 240, 360, 240]),
                'tag_url': subsection.get_absolute_url() if subsection else '/',
                'tag_title': subsection.text if subsection else '',
                'title': unicode(article),
                'byline': byline(article, 'short'),
                'description': article.description
            })

        return JsonResponse({'data': results})

    else:
        raise Http404


@cache_page(settings.CACHE_SHORT)
def section_arts(request):
    """Show the view for the arts section page."""

    nav = 'arts'
    section = Section.cached(nav)
    rss_url = section.rss_url  # url for section's rss feed

    ad_zone = 'content'
    stories = Article.objects.filter(section=section).filter(
        ~Q(tags__text='Arts Blog')).order_by('-created_on')
    books = stories.filter(tags__text='books')
    oncampus = stories.filter(tags__text='on campus')
    music = stories.filter(tags__text='music')
    film = stories.filter(tags__text='film')
    columns = ContentGroup.objects.filter(
        section=section, active=True,
        type='column').annotate(recent=Max('content__issue__issue_date'))
    featured = Article.objects.filter(tags__text='arts front feature') \
        .filter(rel_content__isnull=False) \
        .order_by('-created_on')

    return section.layout.render(request, locals())


@cache_page(settings.CACHE_SHORT)
def section_features(request):
    """Show the view for the arts section page."""

    nav = 'features'
    section = Section.cached(nav)
    ad_zone = 'content'
    return section.layout.render(request, locals())


def section_media(request):
    nav = 'multimedia'
    section = Section.cached(nav)
    rss_url = section.rss_url  # url for section's rss feed

    if request.method == 'GET':
        page = request.GET.get('page', 1)
    else:
        raise Http404

    sort = request.GET.get('sort')
    if sort == 'read':
        RECENT_DAYS = timedelta(days=60)
        newer_than = datetime.now() - RECENT_DAYS
        content = Content.objects \
                         .filter(issue__issue_date__gte=newer_than) \
                         .annotate(hits=Sum('contenthits__hits')) \
                         .order_by('-hits')
    else:
        content = Content.objects.all().order_by('-priority', '-created_on')

    c_type = request.GET.get('type')
    if c_type == 'gallery':
        cts = [Gallery.ct()]
    elif c_type == 'video':
        cts = [Video.ct()]
    else:
        cts = [Video.ct(), Gallery.ct()]
    content = content.filter(content_type__in=cts)

    get_sec = request.GET.get('section')
    if get_sec and 'ajax' in request.GET:
        try:
            s_obj = get_sec.objects.get(name__iexact=get_sec)
            content = content.filter(section=s_obj)
        except:
            pass

    d = paginate(content, page, 6)
    d.update({'nav': nav, 'ad_zone': 'content'})
    d.update({'rss_url': rss_url})

    if 'ajax' in request.GET:
        return render(request, 'ajax/media_viewer_page.html', d)
    else:
        return section.layout.render(request, d)


@cache_page(settings.CACHE_SHORT)
def section_sports(request):
    """Show the view for the sports section page.

    ** There's tons of crap on this page: **
    Athletes of the Week
        3 most recent Articles tagged 'Athlete of the Week'.  For the
        'Athlete of the Week' supplement box
    Latest updates
        Articles listed by most recently updated (great for live coverage)
    Sports blogs
        Blog content.  Don't worry about articles showing up in two places.
    Athlete of the Week
        An article tagged 'athlete of the week'.  Probably higher priority,
        so, exclude this from top stories
    2 sports features
        TODO: not quite sure how to decide which sports to feature
    Sports tags
        unless we add extra data on tags, we'll have to keep a manual list.
    Latest video
        Bam
    Latest scores
        idk yet
    """

    nav = 'sports'
    section = Section.cached(nav)
    rss_url = section.rss_url  # url for section's rss feed

    ad_zone = 'content'

    sportsblog = ContentGroup.objects.get(name='The Back Page')
    raw_stories = Content.objects \
                         .filter(section=section) \
                         .filter(Q(
                             group__isnull=True) |
                             Q(group__isnull=False) & ~Q(group=sportsblog)) \
                         .filter(~Q(tags__text='Sports Front Feature')) \
                         .filter(
                             content_type__model__in=['article',
                                                      'externalcontent']) \
                         .order_by('-created_on')
    latest = Article.objects.filter(section=section) \
                            .order_by('-modified_on') \
                            .filter(
                                ~Q(group=sportsblog) | Q(group__isnull=True))
    blog = raw_stories.filter(group__type='blog')
    scores = Score.objects.order_by('-event_date')[:10]
    sports = Tag.objects.filter(category='sports').order_by('text')
    video = first_or_none(Video.objects.recent.filter(section=section))
    columns = ContentGroup.objects.filter(
        section=section, active=True,
        type='column').annotate(
        recent=Max('content__issue__issue_date')).order_by('-recent')
    columns = columns

    athletes = Article.objects.filter(
        tags__text='Athlete of the Week').order_by('-created_on')
    featured_athlete = None
    for athlete in athletes:
        if get_image_obj(athlete):
            featured_athlete = athlete
            break
    athletes = list(athletes[:3])
    try:
        # Don't want to duplicate featured_athlete
        athletes.remove(featured_athlete)
    except ValueError:
        # Don't worry if featured_athlete isn't in the first three articles
        pass
    athletes = athletes[:2]

    previews = Article.objects.filter(
        tags__text='Previews').order_by('-created_on')
    featured_preview = None
    for athlete in previews:
        if get_image_obj(athlete):
            featured_preview = athlete
            break
    previews = list(previews[:3])
    try:
        # Don't want to duplicate featured_preview
        previews.remove(featured_preview)
    except ValueError:
        # Don't worry if featured_preview isn't in the first three articles
        pass
    previews = previews[:2]

    return section.layout.render(request, locals())


@cache_page(settings.CACHE_STANDARD)
def sports_list(request):
    tags = [
        'Baseball',
        "Men's Basketball",
        "Women's Basketball",
        'Track and Cross Country',
        'Fencing',
        'Field Hockey',
        'Football',
        "Men's Golf",
        "Women's Golf",
        "Men's Crew",
        "Women's Crew",
        "Men's Ice Hockey",
        "Women's Ice Hockey",
        "Men's Lacrosse",
        "Women's Lacrosse",
        "Women's Rugby",
        'Sailing',
        'Skiing',
        "Men's Soccer",
        "Women's Soccer",
        'Softball',
        "Men's Squash",
        "Women's Squash",
        "Men's Swimming",
        "Women's Swimming",
        "Men's Tennis",
        "Women's Tennis",
        "Men's Volleyball",
        "Women's Volleyball",
        "Men's Water Polo",
        "Women's Water Polo",
        'Wrestling'
    ]

    tags_data = []

    for tag_text in tags:
        try:
            tag = Tag.objects.filter(text=tag_text)[0]
        except IndexError:
            continue
        articles = Article.objects.filter(tags=tag).order_by('-created_on')
        if not articles:
            continue
        image = None
        for article in articles:
            if get_image_obj(article):
                should_be_img = True
                for art_tag in article.tags.all():
                    if art_tag.text != tag_text and art_tag.text in tags:
                        should_be_img = False
                        break
                if should_be_img:
                    image = get_image_obj(article)
                    break

        articles = articles[:3]
        article_data = {
            'title': tag.text,
            'main_url': tag.get_absolute_url(),
            'image': image,
            'articles': articles
        }
        tags_data.append(article_data)

    data = {
        'blocks': tags_data,
        'title': 'All Sports',
        'self_url': '/section/sports/list/'
    }

    return render(request, 'block_grid_sports.html', data)


FLYBY_RESULTS_PER_PAGE = 18


@cache_page(settings.CACHE_STANDARD)
def section_arts_blog(request, page=None, tags='Arts Blog'):
    """Display the arts blog."""

    # TODO: figure out what's going on with Section - 'flyby' vs. 'arts'

    nav = 'arts'
    section = Section.cached(nav)

    if not page:
        page = '1'

    subsection = tags.split()[1]
    tag = Tag.objects.filter(text__iexact=tags)[0]
    content = Article.objects.filter(tags=tag).order_by('-created_on')

    featured_content = None
    if page == '1':
        try:

            featured_content = content.filter(
                tags__text='Arts Blog Front Feature')[0]
            if (not featured_content.main_rel_content or
                    not featured_content.main_rel_content.__class__ == Image):
                featured_content = None
        except IndexError:
            featured_content = None

        if not featured_content:
            featured_content = None
            for c in content:
                if (c.main_rel_content and
                        c.main_rel_content.__class__ == Image):
                    featured_content = c
                    break
        if featured_content:
            if content.count() > 1:
                content = content.exclude(id=featured_content.id)
            else:
                featured_content = None

    if not content:
        raise Http404

    # I don't think it's likely that we'll ever have a meaningful
    # distinction of blog/series/column WITHIN flyby, but should it
    # become necessary that can be filtered below
    pager = paginate(content, page, FLYBY_RESULTS_PER_PAGE)
    entries = pager['content']
    p = pager['p']
    paginator = pager['paginator']

    # TODO: change base to arts blog - this controls where you go when
    # you go to new page

    # TODO: change pager to arts blog pager or something

    url_base = '/section/arts/blog'

    ad_zone = 'content'

    return render(request, 'sections/arts_blog.html', locals())


@cache_page(settings.CACHE_SHORT)
def section_flyby(request, page=None, tags=None, cg=None):
    ad_zone = 'content'
    section = Section.cached('flyby')
    if not page:
        page = '1'
    articles = Article.objects.filter(section=section). \
        exclude(title__contains='Harvard Today:').order_by('-created_on')

    if cg:
        articles = articles.filter(group__type=cg.type,
                                   group__name=cg.name)

    paginated_articles = paginate(articles, page, 16)

    return render(request, 'flyby/index.html', {
        'paginated_articles': paginated_articles,
        'cg': cg,
        'nav': 'home' if not cg else '????',
        'ad_zone': ad_zone,
    })


# sponcon1
@cache_page(settings.CACHE_SHORT)
def section_sponsored(request, page=None, tags=None, cg=None):
    section = Section.cached('sponsored')
    articles = Article.objects.filter(section=section).order_by('-created_on')

    return render(request, 'sponsored/the-crimson-brand-studio.html', {
        'articles': articles,
    })


def section_flyby_series(request):
    ad_zone = 'content'
    section = Section.cached('flyby')
    series = ContentGroup.objects.filter(active=True).filter(section=section)

    return render(request, 'flyby/series.html', {
        'series': series,
        'ad_zone': ad_zone,
        'nav': 'series'
    })


ADMISSIONS_PER_PAGE = 12


@cache_page(settings.CACHE_SHORT)
def section_admissions(request, page):
    try:
        page = int(page) - 1
    except (TypeError, ValueError):
        page = 0
    section = Section.cached('admissions')
    admissions_articles = Article.objects.recent.filter(section=section). \
        exclude(tags__text='Admissions Question of the Day')
    featured_articles = admissions_articles.filter(
        tags__text='Admissions Feature')

    start = ADMISSIONS_PER_PAGE * page
    end = start + ADMISSIONS_PER_PAGE
    context = {
        'articles': admissions_articles[start:end],
        'featured': featured_articles[:1],
        'ad_zone': 'content',
    }

    if end < admissions_articles.count():
        context['next_page'] = page + 2

    return section.layout.render(request, context)


def redirect_article_aspx(request):
    try:
        lowercase_get = dict(map(
            lambda key, value: (string.lower(key), value),
            request.GET.items()))
        key = lowercase_get['ref']
        a = Article.objects.get(pk=key)
        return redirect(a, permanent=True)
    except:
        raise Http404


def redirect_writer_aspx(request):
    try:
        lowercase_get = dict(map(
            lambda key, value: (string.lower(key), value),
            request.GET.items()))
        key = lowercase_get['id']
        c = Contributor.objects.get(pk=key)
        return redirect(c, permanent=True)
    except:
        raise Http404


@cache_page(settings.CACHE_STANDARD)
def columns(request, section_name=None):
    columns = ContentGroup.objects.filter(type='column')
    get_keys_lower = map(lambda k: k.lower(), request.GET.keys())
    if 'all' not in get_keys_lower:
        columns = columns.filter(active=True)
    page = 1
    if 'p' in request.GET.keys():
        page = int(request.GET['p'])

    section = None
    if section_name:
        try:
            section = Section.objects.filter(name__iexact=section_name)[0]
            columns = columns.filter(section=section)
        except IndexError:
            raise Http404
    columns = filter(lambda c: Article.objects.filter(group=c).count(),
                     columns)
    if not columns:
        raise Http404

    if section and section.name == 'Sports' and 'all' not in get_keys_lower:
        columns = sorted(
            columns,
            key=lambda g: Article.objects.filter(group=g).order_by(
                '-created_on')[0].created_on,
            reverse=True)
    else:
        columns = sorted(
            columns,
            key=lambda c: Article.objects.filter(group=c)[0]
                                 .contributors.all()[0].last_name)

    p = paginate(columns, page, 15)
    p['first_page'] = 'First'
    p['prev_page'] = 'Previous'
    p['next_page'] = 'Next'
    p['last_page'] = 'Last'
    columns = p['content']

    columns_data = []
    for column in columns:
        column_data = {
            'title': column.name,
            'main_url': column.get_absolute_url(),
            'image': column,
            'articles': Article.objects.filter(group=column)
                                       .order_by('-created_on')[:2]
        }
        columns_data.append(column_data)

    url_base = '/columns'
    title = 'All'
    if section_name:
        url_base += '/' + section_name
        title = section.name
    title += ' Columns'

    url_base += '?'

    active = True
    if 'all' in get_keys_lower:
        url_base += 'all&'
        active = False

    data = {
        'blocks': columns_data,
        'title': title,
        'section_name': section_name if section_name else '',
        'url_base': url_base,
        'active': active
    }

    data.update(p)

    return render(request, 'columnist_block_list.html', data)


@cache_page(settings.CACHE_STANDARD)
def get_content(request, ctype, year, month, day, slug, content_group=None):
    """
    View for displaying a piece of content on a page
    Validates the entire URL
    """

    try:
        c = get_content_obj(request, ctype, year, month, day,
                            slug, content_group)
    except Content.DoesNotExist:
        raise Http404

    # redirect to canonical URL
    c = c.child

    # generate the tagline. To make grammatical sense, will be different
    # depending on whether the contributor has both email and twitter,
    # one of them, or neither.
    if c.content_type.name == 'article' and c.tagline:
        tagline = ''
        for a in c.contributors.all():
            contrib_tag = a.get_tagline(c.byline_type)
            if contrib_tag:
                tagline += '<p>&mdash;%s</p>' % contrib_tag
        c.article.text += tagline

    if request.path != c.get_absolute_url():
        return HttpResponseRedirect(c.get_absolute_url())
    if request.method == 'GET':
        method = request.GET.get('render', 'page')
        if method == 'print':
            method = 'page'  # remove render methods eventually
        return c._render_to_response(method, request=request)
    raise Http404


# sponcon1
@cache_page(settings.CACHE_STANDARD)
def get_sponsored_content(request, ctype, slug, content_group=None):
    ctype = ctype.replace('-', ' ')  # convert from url
    try:
        c = Content.objects.get(slug=slug)
    except ValueError:
        raise Content.DoesNotExist
    c = c.child

    # generate the tagline. To make grammatical sense, will be different
    # depending on whether the contributor has both email and twitter,
    # one of them, or neither.
    if c.content_type.name == 'article' and c.tagline:
        tagline = ''
        for a in c.contributors.all():
            contrib_tag = a.get_tagline(c.byline_type)
            if contrib_tag:
                tagline += '<p>&mdash;%s</p>' % contrib_tag
        c.article.text += tagline

    if request.path != c.get_absolute_url():
        return HttpResponseRedirect(c.get_absolute_url())
    if request.method == 'GET':
        method = request.GET.get('render', 'page')
        if method == 'print':
            method = 'page'  # remove render methods eventually
        return c._render_to_response(method, request=request)
    raise Http404


# no need to cache these two, since they all go through get_content in the end
def get_content_obj(request, ctype, year, month, day, slug,
                    content_group=None):
    """Retrieve a content object from the database (no validation of params)"""
    ctype = ctype.replace('-', ' ')  # convert from url
    try:
        return Content.objects.get(
            issue__issue_date=date(int(year), int(month), int(day)),
            slug=slug)
    except ValueError:
        raise Content.DoesNotExist


def get_grouped_content(request, gtype, gname, ctype, year, month, day, slug):
    """
    View for displaying a piece of grouped content on a page
    Validates the entire url
    """
    # validate the contentgroup
    cg = get_grouped_content_obj(
        request, gtype, gname, ctype, year, month, day, slug)
    if cg:
        return get_content(request, ctype, year, month, day, slug, cg)
    raise Http404


def get_grouped_content_obj(request, gtype, gname, ctype, year, month, day,
                            slug):
    # TODO: i don't think this function is right at all
    return ContentGroup.by_name(gtype, gname)


@cache_page(settings.CACHE_STANDARD)
def get_content_group(request, gtype, gname, page=1, tags=None):
    """Render a Content Group."""
    # validate the contentgroup

    cg = get_content_group_obj(request, gtype, gname)
    if not cg:
        raise Http404
    c = cg.content.all()

    # check if flyby content group - if so, just pass to flyby view
    # if cg.section == Section.objects.get(name='flyby'):
    # ^ this call was not working, replaced with a gtype check 5/1/2016
    # checking gtype prevents backpage from loading. changed to gname 6/14/2016
    if gname == 'flyby':
        return section_flyby(request, page=page)
    # sponcon1
    elif gname == 'sponsored':
        return section_sponsored(request, page=page)
    if tags:
        taglist = tags.split(',')
        tagobjlist = []
        for tag in taglist:
            try:
                tag = Tag.objects.get(text=tag)
                if tag not in tagobjlist:
                    tagobjlist.append(tag)
            except Tag.DoesNotExist:
                pass
        c = c.filter(tags__in=tagobjlist).distinct()
    c = c.order_by('-issue__issue_date', '-modified_on')
    d = paginate(c, page, 5)
    d['cg'] = cg
    d['url_base'] = '/%s/%s' % (gtype, gname)
    # Eventually this should go through filter_helper, but it sucks too
    # much right now
    if tags:
        d['tag_str'] = '/tags/' + ','.join([t.text for t in tagobjlist])
    else:
        d['tag_str'] = ''
    if cg.section:
        d['nav'] = cg.section.name.lower()
    # TODO fix this to not be horrible
    softball = Article.objects.filter(group=cg, tags__text='Softball')
    baseball = Article.objects.filter(group=cg, tags__text='Baseball')
    video = first_or_none(Video.objects.recent.filter(group=cg))
    d['baseball'] = baseball
    d['softball'] = softball
    d['video'] = video
    try:
        loader.get_template(
            'contentgroup/%s/%s/content_list.html' % (gtype, gname))
        t = 'contentgroup/%s/%s/content_list.html' % (gtype, gname)
    except TemplateDoesNotExist:
        t = 'contentgroup.html'
    return render(request, t, d)


def get_content_group_obj(request, gtype, gname):
    return ContentGroup.by_name(gtype, gname)


# sure looks cacheworthy
# @cache(settings.CACHE_STANDARD, "helper")
def filter_helper(req, qs, section_str, type_str, url_base):
    """Return a dictionary with components of content_list filter interface."""

    # TODO: refactor the fuck out of this
    unfilteredcontent = qs
    content = qs
    sects, tps = {}, {}
    o_section_str = section_str

    # parses the comma delimited section_str
    if section_str:
        section_str = [s.lower() for s in section_str.split(',') if s]
        sections = [s for s in Section.objects.all()
                    if s.name.lower() in section_str]
        content = content.filter(section__in=sections)
        show_filter_1 = True
    else:
        section_str = [s.name.lower() for s in Section.objects.all()]
        sections = Section.objects.all()
        show_filter_1 = False
    # generates URLs for the different filter links
    for section in Section.objects.all():
        a = section in sections
        if a:
            s_str = ','.join([s for s in section_str
                              if s != section.name.lower()])
        else:
            s_str = ','.join(section_str + [section.name.lower()])

        url = url_base
        url += ('sections/%s/' % s_str if s_str else '')
        url += ('types/%s/' % type_str if type_str else '')

        # TODO: cache this shit
        ct = len(unfilteredcontent.filter(section=section))
        sects[section.name] = {'selected': a, 'url': url, 'count': ct}

    # models to show in the filter interface... so ghetto
    content_choices = ['article', 'image']
    if type_str:
        type_str = type_str.replace('-', ' ')  # convert from url
        type_str = [t.lower() for t in type_str.split(',')
                    if t in content_choices + ['other']]

        if 'other' in type_str:
            lower_choices = [b.lower() for b in content_choices]
            othertypes = [t for t in Content.types()
                          if t.name not in lower_choices]
        else:
            othertypes = []

        # Models to show
        filter_types = [t for t in Content.types()
                        if t.name.lower() in type_str] + othertypes
        types = type_str
        content = content.filter(content_type__in=filter_types)
        show_filter_2 = True
    # all content types
    else:
        types = content_choices + ['other']
        show_filter_2 = False

    # Iterate over list choices and form URLs
    for type in content_choices + ['other']:
        sel = type in types

        t_str = ','.join([t for t in (types + [type])
                          if t != type or t not in types])

        url = url_base
        url += ('sections/%s/' % o_section_str if o_section_str else '')
        url += ('types/%s/' % t_str if t_str else '')

        if type != 'other':
            curtype = [t for t in Content.types() if t.name.lower() == type][0]
            ct = len(unfilteredcontent.filter(content_type=curtype))
        else:
            lower_choices = [b.lower() for b in content_choices]
            othertypes = [t for t in Content.types()
                          if t.name not in lower_choices]
            ct = len(unfilteredcontent.filter(content_type__in=othertypes))

        if(type in content_choices + ['other']):
            tps[type[0].upper() + type[1:]] = {
                'selected': sel, 'url': url, 'count': ct
            }

    sect_str = '/sections/' + ','.join(section_str) \
        if len(sections) != Section.objects.all().count() else ''
    typ_str = '/types/' + ','.join(types) \
        if len(content_choices) + 1 != len(types) else ''

    return {
        'content': content,
        'sections': sects,
        'section_str': sect_str,
        'types': tps,
        'type_str': typ_str,
        'show_filter': (show_filter_1 or show_filter_2)
    }


def last_month():
    return date.today() + timedelta(days=-30)


def last_year():
    return date.today() + timedelta(days=-365)


@cache_page(settings.CACHE_LONG)
def feature_view(request, title, sectionTitle=None, mediaSlug=None):
    # TODO: Update tags with legit tagnames
    tags = {
        'year-in-sports': {
            'feature': {
                'tag': 'Commencement Feature',
                'title': ''
            },
            'main_stories': {
                'tag': 'Sports Commencement HL',
                'title': ''
            },
            'other_main_stories': {
                'tag': 'Sports Comm Features',
                'title': ''
            },
            'secondary_left': {
                'tag': 'Sports Awards',
                'title': 'Award Winners'
            },
            'secondary_right': {
                'tag': 'Sports Parting Shots',
                'title': 'Sports Parting Shots'
            },
            'tertiary_left': {
                'tag': 'Fall Season Recaps',
                'title': 'Fall'
            },
            'tertiary_middle': {
                'tag': 'Winter Season Recaps',
                'title': 'Winter'
            },
            'tertiary_right': {
                'tag': 'Spring Season Recaps',
                'title': 'Spring'
            },
            'other_stories': {
                'tag': 'Sports Award RU',
                'title': 'Awards Runners-Up'
            }
        },
        '1963-reunion-issue': {
            'feature': {
                'tag': 'Commencement Feature',
                'title': ''
            },
            'main_stories': {
                'tag': 'Secondary Feature',
                'title': ''
            },
            'other_main_stories': {
                'tag': 'Tertiary Feature',
                'title': ''
            },
            'secondary_left': {
                'tag': 'Profiles',
                'title': 'Profiles'
            },
            'secondary_right': {
                'tag': '',
                'title': '1962-1963 Editorials'
            }
        },
        '1988-reunion-issue': {
            'feature': {
                'tag': 'Commencement Feature',
                'title': ''
            },
            'main_stories': {
                'tag': 'Secondary Feature',
                'title': ''
            },
            'other_main_stories': {
                'tag': 'Tertiary Feature',
                'title': ''
            },
            'secondary_left': {
                'tag': 'Profiles',
                'title': 'Profiles'
            },
            'secondary_right': {
                'tag': '',
                'title': '1987-1988 Editorials'
            }
        },
        'senior-section': {
            'feature': {
                'tag': 'Commencement Feature',
                'title': ''
            },
            'main_stories': {
                'tag': 'Wedding3',
                'title': ''
            },
            'other_main_stories': {
                'tag': None,
                'title': ''
            },
            'secondary_left': {
                'tag': '',
                'title': 'Weddings'
            },
            'secondary_right': {
                'tag': 'Letters',
                'title': 'Letters'
            }
        },
        'year-in-review': {
            'feature': {
                'tag': 'Commencement Feature',
                'title': ''
            },
            'main_stories': {
                'tag': 'Side Story',
                'title': ''
            },
            'other_main_stories': {
                'tag': 'Bottom Story',
                'title': ''
            },
            'secondary_left': {
                'tag': '',
                'title': ''
            },
        }
    }

    # Get current section and feature
    feature = get_object_or_404(FeaturePackage, slug=title)
    if feature.pub_status != 1:
        raise Http404
    sections = feature.sections.all()
    currentSection = None
    if sectionTitle is not None:
        currentSection = get_object_or_404(sections, slug=sectionTitle)
    else:
        return redirect('/feature/' + title + '/year-in-review')

    if currentSection.pub_status != 1:
        raise Http404

    relatedItems = PackageSectionContentRelation.objects. \
        filter(FeaturePackageSection=currentSection)

    if 'json' in request.GET:
        from templatetags.content_filters import img_url
        json_content = {
            'url_root': settings.STATIC_URL
        }
        for c in relatedItems:
            if c.related_content.content_type == Gallery.ct:
                photos = []
                for photo in c.related_content.child.contents.all():
                    p = {
                        'caption': photo.child.caption,
                        'thumb_url': img_url(photo.child, '191,1301,191,130'),
                        'med_url': img_url(photo.child, '600,600'),
                        'lightbox_url': img_url(photo.child, '900,900')
                    }
                    photos.append(p)
                json_content[c.related_content.child.title] = photos

        data = 'PHOTO_DATA = ' + json.dumps(json_content, indent=4)
        return HttpResponse(data, content_type='application/json')

    if sectionTitle == 'year-in-photos':
        return render(request, 'year_in_photo.html', {'sections': sections})

    if sectionTitle == 'interactive-map':
        return redirect('http://maps.thecrimson.com')

    if sectionTitle == 'editorial':
        return redirect('/section/opinion')

    rel_tags = dict()
    section_titles = dict()
    for k in tags[sectionTitle].keys():
        rel_tags[k] = tags[sectionTitle][k]['tag']
        section_titles[k] = tags[sectionTitle][k]['title']
    rel_content = dict()

    get_later = None

    for k in rel_tags.keys():
        if rel_tags[k] == '':
            get_later = k
        elif rel_tags is not None:
            items = relatedItems.filter(
                related_content__tags__text=rel_tags[k]) \
                .order_by('order')
            rel_content[k] = [x.related_content.child for x in items]
    if get_later is not None:
        all_items = [x.related_content.child
                     for x in relatedItems.order_by('order')]
        used_items = reduce(lambda acc, elt: acc + elt, rel_content.values())
        to_add = filter(lambda x: x not in used_items, all_items)
        rel_content[get_later] = to_add

    data = {
        'feature': feature,
        'sections': sections,
        'section': sectionTitle,
        'title': currentSection.title,
        'section_titles': section_titles,
        'tags': rel_tags,
        'content': rel_content
    }

    return render(request, 'feature_default.html', data)


def image_watermark(request, imageid):
    image = Image.objects.get(pk=imageid)
    im = PIL.Image.open(image.pic)
    contributors = image.contributors.all()[0]
    return watermark(im, contributors.first_name +
                     '  ' + contributors.last_name)


def issuu_signature(params):
    pairs = sorted(params.items())
    concat_string = ISSUU_API_SECRET + ''.join(k + v for k, v in pairs)
    params['signature'] = hashlib.md5(concat_string).hexdigest()


# cache page for only an hour
@cache_page(60 * 60)
def todays_paper(request):
    payload = {
        'action': 'issuu.documents.list',
        'apiKey': ISSUU_API_KEY,
        'documentStates': 'A',
        'resultOrder': 'desc',
        'format': 'json',
        'pageSize': '1',
        'responseParams': 'documentId,title,username,name',
        'documentSortBy': 'publishDate'
    }

    issuu_signature(payload)
    r = requests.get('http://api.issuu.com/1_0', params=payload)
    doc_id = None
    doc_title = None

    if r.status_code == 200:
        response = r.json()['rsp']
        if response['stat'] == 'ok':
            temp = response['_content']['result']['_content'][0]['document']
            doc_id = temp['documentId']
            doc_title = temp['title']
            doc_user = temp['username']
            doc_name = temp['name']
        else:
            raise Http404
    else:
        raise Http404

    newspaper_link = 'http://issuu.com/{}/docs/{}'.format(doc_user, doc_name)

    volume_information = 'VOLUME CXLV, NO. I'
    if doc_title and doc_title.find('-') >= 0:
        volume_information = doc_title[doc_title.find('-') + 1:].strip()

    payload = {
        'action': 'issuu.document_embeds.list',
        'apiKey': ISSUU_API_KEY,
        'format': 'json',
        'responseParams': 'id',
        'resultOrder': 'desc',
        'pageSize': '1'
    }

    if doc_id is not None:
        payload['docuentId'] = doc_id
    else:
        payload['embedSortBy'] = 'created'

    issuu_signature(payload)

    r = requests.get('http://api.issuu.com/1_0', params=payload)

    embed_id = None
    if r.status_code == 200:
        response = r.json()['rsp']
        if response['stat'] == 'ok':
            data = response['_content']['result']
            if len(data['_content']) > 0:
                embed_id = data['_content'][0]['documentEmbed']['id']
        else:
            raise Http404
    else:
        raise Http404

    embed_html = None
    if embed_id:
        payload = {
            'action': 'issuu.document_embed.get_html_code',
            'apiKey': ISSUU_API_KEY,
            'embedId': str(embed_id)
        }

        issuu_signature(payload)

        r = requests.get('http://api.issuu.com/1_0', params=payload)

        embed_html = r.text

    daily_briefing = LayoutInstance.objects \
                                   .filter(name__contains='Daily Briefing') \
                                   .order_by('-created_on') \
                                   .first()

    placeholders = daily_briefing.placeholders.order_by('position')

    context = {
        'main': placeholders[0],
        'main_content': placeholders[0].content,
        'feat': placeholders[1],
        'feat_content': placeholders[1].content,
        'stories_placeholder': placeholders[2],
        'stories': placeholders[2].content,
        'embedding': embed_html,
        'image': 'https://image.issuu.com/' + str(doc_id) + '/jpg/page_1.jpg',
        'newspaper_link': newspaper_link,
        'volume_information': volume_information
    }

    return render(request, 'todays_paper.html', context)
