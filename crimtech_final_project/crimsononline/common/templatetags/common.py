import datetime
import logging
import re
import urlparse
from re import compile, search
from urllib import urlopen
from xml.dom.minidom import parseString

import django
from django import template
from django.contrib.flatpages.models import FlatPage
from django.db.models import Max
from django.template import defaultfilters as filter
from django.template.loader import render_to_string
from django.utils.safestring import SafeText, mark_safe

from crimsononline.common.utils.html import para_list
from crimsononline.common.utils.lists import first_or_none
from crimsononline.content.models import BreakingNews, Content, Tag, Video
from crimsononline.content_module.models import ContentModule

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter
def paragraphs(str):
    """Split str on <p> tags, mark output as safe.

    Keep the <p> tags in the output.
    """
    return [mark_safe(x) for x in para_list(str)]


@register.filter
def linkify(obj, link_text=''):
    """turns object(s) into (html) link(s).

    if objects have the attr 'domain', stick the domain in the URL.
    """
    try:
        lst = []
        # if obj is not a list, convert it into a list
        if not getattr(obj, '__iter__', False):
            obj = [obj]
        for item in obj:
            if hasattr(item, 'child'):
                item = item.child
            if link_text == '':
                l_text = unicode(item)
            else:
                try:
                    link_text = link_text.encode('ascii')
                    l_text = getattr(item, link_text, link_text)
                except UnicodeEncodeError:
                    l_text = link_text
            if not (isinstance(item, Content) and
                    isinstance(l_text, SafeText)):
                l_text = filter.force_escape(l_text)
            format_args = (item.get_absolute_url(), l_text)
            lst.append(mark_safe('<a href=\'%s\'>%s</a>' % format_args))

        # nonlists obj's should be returned as nonlists
        return lst[0] if len(lst) == 1 else lst
    except:
        return ''


@register.filter
def human_list(lst, connector='and'):
    """turns lst into an comma separated list (with an and)"""
    # we don't want to listify non iterables
    if not getattr(lst, '__iter__', False):
        return lst
    else:
        s = ''
        max_idx = len(lst) - 1
        for i, item in enumerate(lst):
            if i == 0:
                t = '%s'
            elif i == max_idx and max_idx > 1:
                t = ', ' + connector + ' %s'
            elif i == max_idx and max_idx == 1:
                t = ' ' + connector + ' %s'
            else:
                t = ', %s'
            s += t % filter.conditional_escape(item)
        return mark_safe(s)


@register.filter
def return_index_plus1(lst, index):
    try:
        return lst[index + 1]
    except:
        return None


A_LINK_RE = compile(r'href=\"(.+)\"')
A_TEXT_RE = compile(r'>(.+)<')


class FlatpageNavNode(template.Node):
    def __init__(self, nodelist, prefix, cur_url, toplevelonly):
        self.prefix = ('' if prefix.startswith('/') else '/') + prefix
        self.prefix = self.prefix + ('' if prefix[-1] == '/' else '/')
        self.cur_url = template.Variable(cur_url)
        self.nodelist = nodelist
        self.toplevel = toplevelonly
        if self.toplevel:
            self.urldepth = self.prefix.count('/')

    def render(self, context):
        links = []
        splitnodes = self.nodelist.render(context).split('</a>')
        hardlinks = [x + '</a>' for x in splitnodes][:-1]

        for link in hardlinks:
            links.append((search(A_TEXT_RE, link).group(1),
                         search(A_LINK_RE, link).group(1)))
        # print 'lol', links
        pages = FlatPage.objects.filter(url__startswith=self.prefix)
        if self.toplevel:
            pages = [p for p in pages if p.url.count('/') == self.urldepth + 1]
        for page in pages:
            links.append((page.title, page.url))

        links.sort()
        cur_url = self.cur_url.resolve(context)
        # print 'hi', links
        return mark_safe(
            render_to_string('templatetag/flatpagenav.html', locals()))


def do_flatpage_nav(parser, token):
    """Builds a navigation menu for flatpages by url

    inside of the flatpage_nav and endflatpage_nav templatetags, it's
    possible to put static links, which will be sorted and added to the
    navigation

    Usage:
        {% flatpage_nav "/url/root/" "/cur/url" toplevelonly %}
        <a href="/1">link1</a>
        <a href="/2">link2</a>
        {% endflatpage_nav %}

    toplevelonly is optional, and if specified, only adds urls of the form
    "/url/root/.*?/" (eg. omits /url/root/foo/bar/ but includes /url/root/foo/)
    """

    bits = token.split_contents()

    if len(bits) < 3:
        raise template.TemplateSyntaxError(
            '%r tag requires 2 arguments.' % bits[0])

    prefix = bits[1]
    cur_url = bits[2]
    top_level_only = len(bits) > 3 and bits[3] == 'toplevelonly'
    nodelist = parser.parse(('endflatpage_nav',))
    parser.delete_first_token()

    return FlatpageNavNode(nodelist, prefix, cur_url, top_level_only)


register.tag('flatpage_nav', do_flatpage_nav)


@register.inclusion_tag('templatetag/highlights_bar.html')
def highlights_bar():
    """
    Displays the highlights bar on a page. NOTE: this is cached individually
    (see template).
    """
    articles = [c.child
                for c in Content.objects
                                .filter(tags__text='Highlight')
                                .annotate(recent=Max('issue__issue_date'))
                                .order_by('-recent')[:5]]
    return {'articles': articles}


@register.inclusion_tag('templatetag/sponsored_bar.html')
def sponsored_bar():
    """
    Displays the sponsored bar on a page, with the ability to lock ordering
    via sponsored article tags. NOTE: this is cached individually
    (see template).
    """
    articles = []
    articles.extend([c.child
                    for c in Content.objects
                                    .filter(tags__text='Sponsored First')
                                    .annotate(recent=Max('issue__issue_date'))
                                    .order_by('-recent')[:1]])
    articles.extend([c.child
                    for c in Content.objects
                                    .filter(tags__text='Sponsored Second')
                                    .annotate(recent=Max('issue__issue_date'))
                                    .order_by('-recent')[:1]])
    articles.extend([c.child
                    for c in Content.objects
                                    .filter(tags__text='Sponsored Third')
                                    .annotate(recent=Max('issue__issue_date'))
                                    .order_by('-recent')[:1]])
    articles.extend([c.child
                    for c in Content.objects
                                    .filter(tags__text='Sponsored Fourth')
                                    .annotate(recent=Max('issue__issue_date'))
                                    .order_by('-recent')[:1]])
    articles.extend([c.child
                    for c in Content.objects
                                    .filter(tags__text='Sponsored Fifth')
                                    .annotate(recent=Max('issue__issue_date'))
                                    .order_by('-recent')[:1]])
    exclude = ['Sponsored First', 'Sponsored Second', 'Sponsored Third',
               'Sponsored Fourth', 'Sponsored Fifth']
    articles.extend([c.child
                    for c in Content.objects
                                    .filter(tags__text='Sponsored Article')
                                    .exclude(tags__text__in=exclude)
                                    .annotate(recent=Max('issue__issue_date'))
                                    .order_by('-recent')[:5 - len(articles)]])
    """
    Enable this code (and disable the above) for sponsored articles returning
    by date (without the tag preferences)

    articles.extend([c.child
                for c in Content.objects
                                .filter(tags__text='Sponsored Article')
                                .annotate(recent=Max('issue__issue_date'))
                                .order_by('-recent')[:5 - len(articles)]])
    """

    return {'articles': articles}


@register.inclusion_tag('templatetag/sponsored_articles.html')
def sponsored_articles():
    return sponsored_bar()


@register.inclusion_tag('templatetag/date.html')
def date(content):
    modified_date = content.modified_on
    issue_date = content.issue.issue_date

    if datetime.date.today() <= issue_date:
        display_date = modified_date
    else:
        display_date = issue_date

    return {'display_date': display_date, 'modified_date': modified_date}


class WeatherNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        try:
            datasource = urlopen('https://rss.accuweather.com/rss'
                                 '/liveweather_rss.asp?metric=0&locCode=02138')
            wdom = parseString(datasource.read())
            cur_weather = wdom.getElementsByTagName('title')[2]
            cur_weather = cur_weather.childNodes[0].nodeValue
            cur_weather = re.sub(r'(\d{1,3})F', r'\1&deg;F', cur_weather)

            currently = str(cur_weather).split(':')[1].lower()
            icon = ''
            if(currently.count('sun') > 0 or currently.count('clear') > 0):
                if (datetime.datetime.now().hour < 18 and
                        datetime.datetime.now().hour > 6):
                    icon = 'sun.svg'
                else:
                    icon = 'moon.svg'
            elif(currently.count('snow') > 0):
                icon = 'snow.svg'
            elif(currently.count('rain') > 0):
                icon = 'rain.svg'
            elif(currently.count('cloud') > 0):
                icon = 'cloud.svg'
            if icon:
                icon_txt = ('<img alt="%s" src="%s" width="16" height="16" '
                            'style="vertical-align:bottom; margin-left:2px;"/>'
                            % (icon.split('.')[0],
                               django.conf.settings.STATIC_URL +
                               'images/icons/' + icon))
            else:
                icon_txt = ''
            return ('<a href="https://www.accuweather.com/en/us/cambridge-ma/'
                    '02138/weather-forecast/756_pc">'
                    '<span class="weather-locale">Cambridge, MA</span> '
                    'Weather: {} {}</a>'
                    .format(str(cur_weather).split()[-1], icon_txt))
        except:
            # Don't raise exception if feed is down or something else
            return ''


def weather(parser, token):
    """A little weather widget (displays the temp) for the subnav."""
    bits = token.split_contents()
    return WeatherNode(*(bits[1:3]))


weather = register.tag(weather)


class TaglinksNode(template.Node):
    def __init__(self, linklist, urlbase):
        self.linklist = linklist
        self.urlbase = template.Variable(urlbase)

    def render(self, context):
        try:
            self.urlbase = self.urlbase.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        return render_to_string(
            'templatetag/taglinks.html',
            {'linklist': self.linklist, 'url_base': self.urlbase})


def taglinks(parser, token):
    """
    Renders an ad using the OpenX Account
    """
    bits = token.split_contents()

    if len(bits) != 3:
        raise template.TemplateSyntaxError(
            '%r tag requires 1 argument.' % bits[0])
    cmname = bits[1]

    try:
        srcm = ContentModule.objects.get(name=cmname)

        inputstrl = srcm.comment.strip().split('\n')
        tuplelist = []
        for tagset in inputstrl:
            tuplelist.append((tagset.split('=')[0].strip(),
                             tagset.split('=')[1].strip()))

    except:
        tuplelist = []
    urlbase = bits[2]

    return TaglinksNode(tuplelist, urlbase)


taglinks = register.tag(taglinks)


@register.simple_tag
def latest_tagged_video(tag):
    """
    Returns the key of the latest video with the tag specified.
    """
    if not isinstance(tag, Tag):
        try:
            tag = Tag.objects.get(text=tag)
        except Tag.DoesNotExist:
            return mark_safe('')
    video = first_or_none(Video.objects.filter(tags=tag)
                                       .order_by('-issue__issue_date'))
    if video:
        return mark_safe(video.key)
    return mark_safe('')


@register.inclusion_tag('templatetag/breaking_news.html')
def breaking_news():
    try:
        news = BreakingNews.objects.get()
    except BreakingNews.DoesNotExist, BreakingNews.MultipleObjectsReturned:
        news = None
    return {'news': news}


@register.filter
def absolute_url(url):
    if url.startswith('https://') or url.startswith('https://'):
        return url
    else:
        return urlparse.urljoin('https://www.thecrimson.com/', url.lstrip('/'))


@register.filter
def flatten_list(lst, key=None):
    """
    http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-
    list-of-lists-in-python
    """
    if not key:
        return [item for sublist in lst for item in sublist]
    try:
        return [item for sublist in lst for item in sublist[key]]
    except TypeError:
        return [item for sublist in lst for item in
                sublist.__getattribute__(key)]


@register.filter
def following(lst, content):
    """Returns the list of items following `content`, wrapping around"""
    if content not in lst:
        return lst
    i = lst.index(content) + 1
    # Hacky way of wrapping around
    return (lst + lst)[i:i + len(lst) - 1]


@register.filter
def get_range(value):
    return range(value)


@register.filter
def preceding(lst, content):
    """Returns the list of items preceding `content`, wrapping around"""
    if content not in lst:
        return lst
    i = lst.index(content) + len(lst) - 1
    # Hacky way of wrapping around
    return (lst + lst)[i - len(lst):i - 1]
