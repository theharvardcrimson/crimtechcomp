import copy
import csv
import json
import logging
import os
import re
import urllib
import urllib2
from datetime import date, datetime, time
from os.path import splitext
from re import DOTALL, compile, sub

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.files.base import ContentFile
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q, permalink
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template import RequestContext, TemplateDoesNotExist
from django.template.defaultfilters import truncatewords
from django.template.loader import get_template, render_to_string
from django.utils.datetime_safe import strftime as strftime_safe
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag as BSTag
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.files import get_thumbnailer
from model_utils.managers import InheritanceManager
from solo.models import SingletonModel

from crimsononline.common.caching import expire_all, expire_page
from crimsononline.common.utils.cropping import size_spec_to_size
from crimsononline.common.utils.misc import ret_on_fail
from crimsononline.common.utils.strings import (
    make_file_friendly, make_url_friendly, rand_str)
from crimsononline.common.utils.urlnames import urlname
from crimsononline.content.generators import (
    generate_rec_articles_task, get_keywords_task)
from crimsononline.shortcodes import parser

logger = logging.getLogger(__name__)


def add_issue_filter(f):
    """Modify a manager method to add a filter for restricting by issue date.

    Adds the ability to process (optional) start and end dates
    """
    def f_prime(*args, **kwargs):
        start = kwargs.pop('start', None)
        end = kwargs.pop('end', None)
        if start is None and end is None:
            return f(*args, **kwargs)
        q = {}
        if start:
            if isinstance(start, datetime):
                start = start.date()
            q['issue__issue_date__gte'] = start
        if end:
            if isinstance(end, datetime):
                end = end.date()
            q['issue__issue_date__lte'] = end
        return f(*args, **kwargs).filter(**q)
    return f_prime


class ContentManager(models.Manager):
    """Base class for managers of Content derived objects."""

    # TODO: make this date crap into a decorator or something

    @add_issue_filter
    def get_queryset(self):
        return self.all_objects().filter(pub_status=1)

    @add_issue_filter
    def all(self):
        return self.get_queryset()

    @add_issue_filter
    def all_objects(self):
        return super(ContentManager, self).get_queryset()

    @add_issue_filter
    def admin_objects(self):
        return self.all_objects().select_related().exclude(pub_status=-1)

    @add_issue_filter
    def draft_objects(self):
        return self.all_objects().select_related().filter(pub_status=0)

    @add_issue_filter
    def deleted_objects(self):
        return self.all_objects().select_related().filter(pub_status=-1)

    @property
    def recent(self):
        return self.get_queryset().order_by('-created_on')

    def prioritized(self, recents=7):
        """Order by (priority / days_old).

        Arguments:
            recents=N => only return stuff from the past N issues. this should
                make the query have a reasonable run time.
        """
        issue_pks = [str(i.pk) for i in Issue.last_n(recents)]
        future_issues = Issue.objects.filter(issue_date__gt=date.today()) \
                                     .order_by('-issue_date')
        # include issues in future
        issue_pks = [str(i.pk) for i in future_issues] + issue_pks

        age_expr = '(TIMESTAMPDIFF(HOUR, content_content.created_on, NOW())+1)'

        qs = self.get_queryset().extra(
            select={
                'decayed_priority': 'content_content.priority / ' + age_expr
            },
            where=[
                'content_issue.id = content_content.issue_id',
                'content_issue.id in (%s)' % ', '.join(issue_pks)
            ],
            tables=['content_issue']
        )
        return qs.extra(order_by=['-decayed_priority'])

    def featured(self, default=None):
        article = self.recent.filter(tags__text='Front Feature')
        if article.exists():
            return article[0]
        else:
            return default


class SContentManager(ContentManager, InheritanceManager):
    pass


class Content(models.Model):
    """Base class for all content.

    Has some content rendering functions and property access methods.
    """

    PUB_CHOICES = (
        (0, 'Draft'),
        (1, 'Published'),
        (-1, 'Deleted'),
    )
    PRIORITY_CHOICES = (
        (1, '1 | one off articles'),
        (2, '2 |'),
        (4, '3 | a normal article'),
        (5, '4 |'),
        (6, '5 |'),
        (7, '6 | kind of a big deal'),
        (9, '7 | lasts ~2 days'),
        (13, '8 |'),
        (17, '9 | ~ 4 days'),
        (21, '10 | OMG, It\'s Faust!'),
    )

    title = models.CharField(
        max_length=200, blank=False, null=False, default='')

    ### DUDE totally don't forget to add a subtitle field with max length of 255, blank true, null false, and default of blank string, thanks!
    
    description = models.TextField(blank=True, null=False, default='')
    contributors = models.ManyToManyField('Contributor',
                                          related_name='content')
    multimedia_contributors = models.ManyToManyField(
        'Contributor', related_name='multimedia_content')
    contributor_override = models.TextField(
        blank=True, null=False, default='',
        help_text='Custom HTML to use in place of the auto-generated '
                  'contributor titles and names. Available only on certain '
                  'templates.')
    tags = models.ManyToManyField(
        'Tag', related_name='content', blank=True)
    issue = models.ForeignKey('Issue', null=False, related_name='content')
    slug = models.SlugField(
        max_length=70, help_text="""
        The text that will be displayed in the URL of this article.
        Can only contain letters, numbers, and dashes (-).
        """
    )
    section = models.ForeignKey('Section', null=False, related_name='content')
    priority = models.IntegerField(
        default=3, choices=PRIORITY_CHOICES,
        db_index=True)
    group = models.ForeignKey(
        'ContentGroup', null=True, blank=True,
        related_name='content')
    pub_status = models.IntegerField(
        null=False, choices=PUB_CHOICES,
        default=0, db_index=True)
    original_pub_status = None
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_on = models.DateTimeField(db_index=True)
    old_pk = models.IntegerField(null=True, help_text='primary key '
                                 'from the old website.', db_index=True)
    searchable = models.BooleanField(
        blank=False, default=True, db_index=True,
        help_text='Allow search engines to index this content')
    paginate = models.BooleanField(
        default=True, null=False, blank=True,
        help_text='Allow article to be paginated')
    show_ads = models.BooleanField(blank=False, default=True)

    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    def __init__(self, *args, **kwargs):
        super(Content, self).__init__(*args, **kwargs)
        self.original_pub_status = self.pub_status

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(
                self.__class__)
        if self.pk is None or not kwargs.pop('keep_modified_on', False):
            self.modified_on = datetime.now()
        retval = super(Content, self).save(*args, **kwargs)
        # expire own page
        expire_page(self.get_absolute_url())
        expire_page('/robots.txt')  # update robots.txt in case unsearchable
        for i in range(1, 21):
            expire_page('{}?page={}'.format(self.get_absolute_url(), i))
        expire_page('{}?page=single'.format(self.get_absolute_url()))
        # we should expire the section page for the content type if it has one
        expire_page(self.section.get_absolute_url())
        # writer page for the contributor of the content
        for contributor in self.contributors.all():
            expire_page(contributor.get_absolute_url())
        # contentgroup page? I DON'T EVEN KNOW
        if self.group is not None:
            expire_page(self.group.get_absolute_url())
        # all the tag pages woo
        for tag in self.tags.all():
            expire_page(tag.get_absolute_url())

        # expire the arts blog if needed
        if len(self.tags.filter(text='Arts Blog')) >= 1:
            expire_page(reverse('content.section.arts.blog'))

        # expire march madness feature
        mad_tags = ['March Madness Feature', 'March Madness Feature Left',
                    'March Madness Feature Right', 'March Madness Left',
                    'March Madness Right', 'From the Bench',
                    'Around the Tournament', 'Breaking it Down']
        q = Q()
        for t in mad_tags:
            q |= Q(text=t)
        if len(self.tags.filter(q)) > 0:
            expire_page(reverse('crimsononline.march_madness.views.index'))
        self.original_pub_status = self.pub_status
        return retval

    @classmethod
    def ct(cls):
        """Returns the content type for this class.

        Note that ContentType.objects already caches
        """
        return ContentType.objects.get_for_model(cls)

    @property
    def num_comments(self):
        page_url = '%s%s' % (
            'https://www.thecrimson.com/', self.get_absolute_url()[1:])
        disqus_thread_url = 'https://disqus.com/api/get_thread_by_url' \
                            '?forum_api_key=%s&url=%s' % (
                                settings.DISQUS_FORUM_KEY, page_url)
        cache_key = page_url + '!num_comments'

        num_comments = 0
        try:
            num_comments = cache.get(cache_key)
            if num_comments is None:
                num_comments = json.load(urllib.urlopen(
                    disqus_thread_url))['message']['num_comments']
                cache.set(cache_key, num_comments, 1800)
        except:
            pass
        if num_comments is None:
            num_comments = 0

        return num_comments

    @property
    def child(self):
        """
        Return the instance of the child class.

        If c (an instance of Content) was an article, c.child would be
        equivalent to c.article
        """
        child_name = self.content_type.name.lower().replace(' ', '')
        try:
            return getattr(self, child_name)
        except ObjectDoesNotExist:  # db integrity error
            # parent exists, but child doesn't exist.  since the child data
            #  doesn't exist, might as well delete the parent to prevent
            #  further errors
            self.delete()
            raise

    class Meta:
        unique_together = (
            ('issue', 'slug'),
        )
        permissions = (
            ('content.can_publish', 'Can publish content',),
            ('content.can_unpublish', 'Can unpublish content',),
            ('content.can_delete_published', 'Can delete published content'),
            ('make_unsearchable_content',
                'Can hide content from search engines'),
            ('can_hide_ads', 'Can prevent ads from displaying on content')
        )
        get_latest_by = 'created_on'

    @permalink
    def get_absolute_url(self):
        i = self.issue.issue_date
        url_data = [
            self.content_type.name.replace(' ', '-'), i.year,
            i.month, i.day, self.slug]
        if self.section == Section.cached('admissions'):
            return ('content_admissions', url_data)
        elif self.content_type.name == 'topic page':
            return ('content_topic', [self.child.get_slug_path()])
        elif self.section == Section.cached('flyby'):
            return ('content_flyby', url_data)
        # sponcon1
        elif self.section == Section.cached('sponsored'):
            url_data = [self.content_type.name.replace(' ', '-'), self.slug]
            return ('content_sponsored', url_data)
        elif self.group:
            url_data = [
                self.group.type.lower(),
                make_url_friendly(self.group.name)] + url_data
            return ('content_grouped_content', url_data)
        else:
            return ('content_content', url_data)

    def get_full_url(self):
        """ includes domain """
        return '%s%s' % (settings.URL_BASE, self.get_absolute_url()[1:])

    def get_admin_change_url(self):
        return urlresolvers.reverse('admin:content_%s_change'
                                    % str(self.content_type).replace(' ', '_'),
                                    args=(self.pk,))

    def __unicode__(self):
        if self.content_type:
            return self.child.__unicode__()
        else:
            return self.title

    def subsection(self):
        # Pretend like we have "subsections" by returning first uncategorized
        # tag. TODO: fix this.
        tags = self.tags.all()
        if tags.exists():
            return tags[0]

    def fm_subsection(self):
        for tag in self.tags.all():
            if tag.text in ['Issues', 'Levity', 'Retrospection', 'The Scoop',
                            'Conversations', 'Introspection', 'Around Town']:
                return tag
        return self.subsection()

    objects = ContentManager()
    sobjects = SContentManager()

    def get_template_for_method(self, method, name, ext):
        if ((self.content_type.name == 'article' or
                self.content_type.name == 'gallery') and
                self.child.layout_instance and method == 'page'):
            templ = self.child.layout_instance.parent.template_path
        elif self.group:  # TODO fix this block to not be horrible
            try:
                templ = (
                    'models/%s/contentgroup/%s/%s/%s%s' %
                    (name, self.group.type, make_url_friendly(self.group.name),
                     method, ext))
                # The call to get_template is to raise
                # TemplateDoesNotExist if, in fact, the template doesn't
                # exist.  Its return value isn't used.
                get_template(templ)
                return (templ, '/%s/%s' % (
                        self.group.type, make_url_friendly(self.group.name)))
            except TemplateDoesNotExist:
                templ = 'models/%s/%s%s' % (name, method, ext)
        else:
            templ = 'models/%s/%s%s' % (name, method, ext)
        return (templ, None)

    def _render(self, method, context=None, request=None, **kwargs):
        """
        Render to some kind of string (usually HTML), depending on method

        Always uses the child class

        method -- Specification for the render; it could be something like,
            'admin' or 'search'
        context -- gets injected into template (optional)
        """
        from crimsononline.common.templatetags.common import paragraphs

        if not context:
            context = {}

        # if self.content_type.name == 'External Content':
        #     kwargs['ctype'] = self.child.repr_type
        n_context = copy.copy(context)
        nav = self.section.name.lower()
        name = kwargs.pop('ctype', self.content_type) \
                     .name \
                     .lower().replace(' ', '')
        ext = '.html' if method[-4:] != '.txt' else ''

        if self.content_type == ContentType.objects.get_for_model(Map):
            n_context.update({'google_api_key': settings.GOOGLE_API_KEY})

        if self.content_type == ContentType.objects.get_for_model(Widget):
            rend_html = re.sub(r'\{\{ *STATIC_URL *\}\}', settings.STATIC_URL,
                               self.child.html)
            rend_html = re.sub(r'\{\{\ *id *\}\}', 'container1', rend_html)
            rend_js = re.sub(r'\{\{ *STATIC_URL *\}\}', settings.STATIC_URL,
                             self.child.javascript)
            rend_js = re.sub(r'\{\{\ *id *\}\}', 'container1', rend_js)
            n_context.update({'rendered_html': rend_html,
                              'rendered_js': rend_js})

        if self.group and self.group.type == 'series':
            series = [
                c.child for c in
                Content.objects.all_objects()
                .filter(group__type=self.group.type,
                        group__name=self.group.name)
                .order_by('issue__issue_date')]
            n_parts = len(series)
            idx = series.index(self)
            if idx < 2:
                start = 0
                end = min(n_parts, 5)
            elif idx > n_parts - 3:
                start = max(n_parts - 5, 0)
                end = n_parts
            else:
                start = idx - 2
                end = idx + 3
            five = series[start:end]
            series_nums = range(start + 1, end + 2)
            n_context['series_articles'] = zip(series_nums, five)

        if self.content_type == ContentType.objects.get_for_model(Article):
            # Find next/prev articles
            main_tag = self.tags.filter(text__in=[
                'Faculty News', 'College News', 'University News', 'Metro News'
            ]).first()
            article_date = self.created_on
            prev_query = Article.objects.filter(created_on__lt=article_date) \
                .exclude(title=self.title)
            next_query = Article.objects.filter(created_on__gt=article_date) \
                .exclude(title=self.title)
            # Note: this assumes that all News articles have one of the four
            # main tags
            if main_tag:
                prev_query = prev_query.filter(tags__text__contains=main_tag)
                next_query = next_query.filter(tags__text__contains=main_tag)
            # Handle other sections here. Note: possible missed case here if
            # this article is in News, but isn't properly tagged
            else:
                prev_query = prev_query.filter(section=self.section)
                next_query = next_query.filter(section=self.section)
            prev_article = prev_query.order_by('-created_on').first()
            next_article = next_query.order_by('created_on').first()

            if next_article == self:
                next_article = None

            n_context['prev'] = prev_article
            n_context['next'] = next_article
            # if main_tag == None, then set it to the section name
            n_context['main_tag'] = main_tag or self.section.name
            # Read about coalescing operators here: https://goo.gl/fBlN5R
            # This is common in Javascript, C#, and other languages

            # Find BFs
            soup = BeautifulSoup(self.article.text.replace(
                '<p>&nbsp;</p>', ''))
            n_context['nav_sections'] = []
            count = 0
            for bf in soup.findAll(['h2', 'h3']):
                tag_id = 'article-nav-section-%d' % (count,)
                n_context['nav_sections'].append((tag_id, bf.text))
                anchor = BSTag(soup, 'a')
                anchor['id'] = tag_id
                anchor['class'] = 'nav-section-anchor'
                bf.insert(0, anchor)
                count += 1

            # parser.parse here is the shortcodes parser
            paragraphs = paragraphs(parser.parse(soup.renderContents()))

            if request is None:
                page = 1
            else:
                page = request.GET.get('page', 1)

            if (self.section == Section.cached('admissions') or
                    self.section == Section.cached('magazine')):
                page = 'single'

            templs = ['placeholders/hpac.html', 'placeholders/hpac_dark.html']
            if (hasattr(self, 'layout_instance') and self.layout_instance and
                    self.layout_instance.parent.template_path in templs):
                page = 'single'

            if page != 'single' and self.paginate:
                paginator = Paginator(paragraphs, 15, orphans=5)
                try:
                    paragraphs = paginator.page(page)
                except EmptyPage:
                    paragraphs = paginator.page(paginator.num_pages)
                except PageNotAnInteger:
                    paragraphs = paginator.page(1)

            # also stores whether a paragraph is holds a bf
            annotated_paragraphs = []
            slideshow_img_idxs = []
            count = 0
            n_context['is_slideshow'] = False
            for idx, para in enumerate(paragraphs):
                soup = BeautifulSoup(para)
                cur = soup.find(['h2', 'h3'])
                if cur is not None:
                    annotated_paragraphs.append([para, count])
                    count += 1
                else:
                    fullscreen = soup.find('div',
                                           'shortcodes-wrapper-fullscreen')
                    if soup.p and fullscreen:
                        annotated_paragraphs.append(
                            [re.sub(r'</?p>', '', para), -1])
                    else:
                        annotated_paragraphs.append([para, -1])

                if soup.find('div', 'shortcodes-wrapper-slideshow'):
                    n_context['is_slideshow'] = True
                    if soup.find('img') or soup.find('iframe'):
                        slideshow_img_idxs += [idx]

            n_context['paragraphs'] = paragraphs
            n_context['annotated_paragraphs'] = annotated_paragraphs
            n_context['bf_count'] = count
            n_context['bf_mid'] = count / 2
            if n_context['is_slideshow']:
                try:
                    n_context['ad_idx_first'] = slideshow_img_idxs[2]
                    n_context['ad_idx_second'] = slideshow_img_idxs[5]
                except IndexError:
                    pass
            else:
                n_context['ad_idx_first'] = len(annotated_paragraphs) / 4
                n_context['ad_idx_second'] = len(annotated_paragraphs) * 3 / 4
            n_context['tags'] = [{
                'url': t.get_absolute_url(),
                'text': t.text.replace(' ', '&nbsp;')
            } for t in self.tags.all()]
            main_rel = self.child.main_rel_content
            if main_rel and main_rel.content_type.name == 'image':
                n_context['main_rel_content_too_tall'] = \
                    main_rel.height > main_rel.width

        # this is slightly horrible, but basically we check to see if there
        # is a template under an extcont's represented content before failing
        templ, new_base = self.get_template_for_method(method, name, ext)
        if name == 'externalcontent':
            try:
                get_template(templ)
            except TemplateDoesNotExist:
                logger.info(
                    'External content for type %s falling back to %s template'
                    % ((self.child.repr_type,) * 2))
                name = self.child.repr_type.name.lower().replace(' ', '')
                templ, new_base = self.get_template_for_method(
                    method, name, ext)

        if new_base is not None:
            n_context['url_base'] = new_base

        # dumb hack for this jerk
        if self.slug in ['news-in-brief-student-charged-with',
                         'police-arrest-junior-for-assault-span',
                         'four-undergrads-face-drug-charges-span',
                         'students-plead-not-guilty-to-drug',
                         'judge-sets-next-date-in-marijuana',
                         'judge-moves-to-dismiss-dewolfe-drug',
                         'judge-may-dismiss-dewolfe-drugs-case',
                         'mcginn-n-tonic-revisiting-harvard-football',
                         'hefs-got-nothin-on-harvards-hottest',
                         'leave-of-absence-harvard',
                         'police-arrest-student-for-possession-of',
                         'color-line-cuts-through-the-heart',
                         'scoped-jordan-b-weitzen-08-span',
                         'student-arrested-for-quad-break-in-after']:
            noindex = True
        else:
            noindex = False

        # TODO: Allow this to be specified via the admin
        # can access self with either the name of the class (ie, 'article')
        #   or 'content'
        pcrs = PackageSectionContentRelation.objects.filter(
            related_content=self)
        if len(pcrs) > 0:
            featureStr = pcrs[0].FeaturePackageSection.MainPackage.title
            featureSlug = pcrs[0].FeaturePackageSection.MainPackage.slug
            sectionStr = pcrs[0].FeaturePackageSection.title
            sectionSlug = pcrs[0].FeaturePackageSection.slug
            n_context.update({
                'feature': featureStr,
                'fSection': sectionStr,
                'featureSlug': featureSlug,
                'sectionSlug': sectionSlug})

        n_context.update({
            name: self.child,
            'content': self.child,
            'class': name,
            'disqus': settings.DISQUS,
            'nav': nav,
            'noindex': noindex,
            'ad_zone': 'content'})

        if method == 'page':
            # flyby content
            if (self.section == Section.cached('flyby') and
                    self.content_type == Article.ct()):
                # TODO: This is bad; fix it
                section = self.section
                series = list(ContentGroup.objects.filter(active=True).filter(
                    section=section))
                from crimsononline.common.utils.lists import first_or_none
                video = first_or_none(
                    Video.objects.recent.filter(section=section))
                n_context.update({'section': section,
                                  'series': series,
                                  'video': video})
                return mark_safe(render_to_string('models/%s/flyby.page.html'
                                 % name,
                                 n_context,
                                 context_instance=RequestContext(request)))

            if ((self.section == Section.cached('magazine') and
                    self.content_type == Article.ct()) and
                    not self.layout_instance):
                section = self.section
                n_context.update({'section': section})
                return mark_safe(render_to_string('models/%s/fm.page.html'
                                 % name,
                                 n_context,
                                 context_instance=RequestContext(request)))

            if (self.section == Section.cached('admissions') and
                    self.content_type == Article.ct()):
                section = self.section
                series = list(ContentGroup.objects.filter(active=True).filter(
                    section=section))
                from crimsononline.common.utils.lists import first_or_none
                video = first_or_none(Video.objects.recent.filter(
                    section=section))
                if 'paragraphs' in n_context:
                    n_context['paragraphs'] = n_context['paragraphs']
                n_context.update({'section': section,
                                  'series': series,
                                  'video': video})
                return mark_safe(render_to_string(
                    'models/%s/admissions_full.html' % (name),
                    n_context, context_instance=RequestContext(request)))

        rc = None
        if request:
            rc = RequestContext(request)

        return mark_safe(render_to_string(
            templ, n_context, context_instance=rc))

    def _render_to_response(self, method, context=None, request=None,
                            **kwargs):
        return HttpResponse(self._render(method, context, request))

    def delete(self):
        # anyone can delete drafts
        if int(self.pub_status) is 0:
            super(Content, self).delete()
        else:
            self.pub_status = -1
            self.save()

    @staticmethod
    # @funcache(3600)
    def types():
        """Return all ContentType objects with parent Content"""
        arr = [ContentType.objects.get_for_model(cls)
               for cls in Content.__subclasses__()]
        arr.remove(ContentType.objects.get_for_model(ExternalContent))
        return arr


class ContentHits(models.Model):
    content = models.ForeignKey(Content, db_index=True)
    date = models.DateField(auto_now_add=True, db_index=True)
    hits = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return 'Content %d with %d hits' % (self.content_id, self.hits)


def get_img_path(instance, filename):
    ext = splitext(filename)[1]
    safe_name = make_file_friendly(instance.name)
    return 'photos/contentgroups/%s/%s%s' % (instance.type, safe_name, ext)


class ContentGroup(models.Model):
    """
    Groupings of content.  Best for groupings that have simple metadata
        (just a blurb and an image), arbitrary (or chronological) ordering,
        and not much else.
    This is different from tags because groupings have metadata.

    Examples:
      * Columns
      * Blogs
      * Feature (say, a series on Iraq or the election)
    """
    TYPE_CHOICES = (
        ('column', 'Column'),
        ('series', 'Series'),
        ('blog', 'Blog'),
    )

    DAY_CHOICES = (
        ('m', 'Monday'),
        ('t', 'Tuesday'),
        ('w', 'Wednesday'),
        ('th', 'Thursday'),
        ('f', 'Friday')
    )

    WEEK_CHOICES = (
        ('one', 'Week One'),
        ('two', 'Week Two'),
        ('three', 'Week Three')
    )

    type = models.CharField(max_length=25, choices=TYPE_CHOICES, db_index=True)
    name = models.CharField(max_length=70, db_index=True)
    subname = models.CharField(max_length=40, blank=True, null=True)

    blurb = models.TextField(blank=True, null=True)
    section = models.ForeignKey('Section', blank=True, null=True)
    image = models.ImageField(
        upload_to=get_img_path, blank=True, null=True,
        help_text='Thumbnail')
    active = models.BooleanField(
        default=True, help_text='ContentGroups that '
        'could still have content posted to them are active.  Active '
        'blogs and columnists show up on section pages.', db_index=True)
    day_of_week = models.CharField(
        blank=True, null=True, choices=DAY_CHOICES,
        max_length=70, help_text='Day of week they publish')
    week = models.CharField(
        blank=True, null=True, choices=WEEK_CHOICES,
        max_length=20, help_text='What week do they publish')

    class Meta:
        unique_together = (('type', 'name',),)

    def __unicode__(self):
        return '%s/%s' % (self.type, self.name)

    def delete(self):
        self.content.clear()
        super(ContentGroup, self).delete()

    def display_url(self, size_spec):
        """ convenience method for the pic attribute's method of same name """
        try:
            width, height = size_spec_to_size(
                size_spec, self.image.width, self.image.height)
        except IOError:
            if settings.DOWNLOAD_UPSTREAM_MEDIA:
                download_upstream(self.image)
                width, height = size_spec_to_size(
                    size_spec, self.image.width, self.image.height)
            else:
                raise
        grad_data = {'grad': False}
        if 'GRAD' in size_spec:
            grad_specs = size_spec[size_spec.index('GRAD') + 1:]
            grad_data = {
                'grad': True,
                'color': grad_specs[0],
                'max_opacity': grad_specs[1],
                'min_opacity': grad_specs[2],
                'direction': grad_specs[3]
            }

        options = {'size': (width, height), 'crop': 'smart', 'upscale': True}
        options = dict(options.items() + grad_data.items())
        return get_thumbnailer(self.image).get_thumbnail(options).url

    @staticmethod
    def by_name(type, name):
        """
        Find CGs by type, name key.
        Content Groups shouldn't change that much. We cache them.
        """
        cg = cache.get('contentgroups_all')
        # If contentgroups_all has expired, get it again
        if not cg:
            cg = ContentGroup.update_cache()
            cg_refreshed = True
        else:
            cg_refreshed = False
        # We expect that most of the calls to by_name will be for groups that
        # actually exist, so if a group isn't found in the cached list, we
        # refresh the cache and look again.
        obj = cg.get((type, name), None)
        if not obj and not cg_refreshed:
            cg = ContentGroup.update_cache()
            obj = cg.get((type, name), None)
        return obj

    @staticmethod
    def update_cache():
        """
        This is a separate method, since we want to be add update
        the cache if we create a new content group
        """
        cg = {}
        objs = ContentGroup.objects.all()[:]
        for obj in objs:
            cg[(obj.type, make_url_friendly(obj.name))] = obj
        cache.set('contentgroups_all', cg, 1000000)
        return cg

    def save(self, *args, **kwargs):
        """
        When Content Groups change, we need to update the cache
        """
        s = super(ContentGroup, self).save(*args, **kwargs)
        try:
            # expire own page
            expire_page(self.get_absolute_url())
            # we should expire the section pag for the content type if
            # it has one
            if(self.section):
                expire_page(self.section.get_absolute_url())
            ContentGroup.update_cache()
        except:
            raise
        return s

    @permalink
    def get_absolute_url(self):
        if self.section == Section.cached('flyby'):
            return (
                'flyby_content_contentgroup',
                [self.type, make_url_friendly(self.name)])
        return (
            'content_contentgroup', [self.type, make_url_friendly(self.name)])


class Tag(models.Model):
    """
    A word or phrase used to classify or describe some content.

    # A bit of setup
    >>> from django.db import IntegrityError

    # Create some tags
    >>> tag1 = Tag.objects.create(text='potato')
    >>> tag2 = Tag.objects.create(text='not potato')

    # No duplicate tags
    >>> try:
    ...     tag3 = Tag.objects.create(text='potato')
    ... except IntegrityError:
    ...     print "caught"
    ...
    caught

    # __unicode__
    >>> str(tag1)
    'potato'
    """

    CATEGORY_CHOICES = (
        ('sports', 'Sports'),
        ('college', 'College'),
        ('faculty', 'Faculty'),
        ('university', 'University'),
        ('city', 'City'),
        ('stugroups', 'Student Groups'),
        ('houses', 'Houses'),
        ('depts', 'Departments'),
        ('', 'Uncategorized')
    )

    # validates in the admin
    text = models.CharField(
        blank=False, max_length=40, unique=True,
        help_text='Tags can contain letters and spaces', db_index=True)
    category = models.CharField(blank=True, max_length=25,
                                choices=CATEGORY_CHOICES, db_index=True)
    is_vague = models.BooleanField(
        default=False,
        help_text='Vague tags are those that are too broad or so widely \
                used that they should not be taken into account when \
                recommended articles are generated.')

    def __unicode__(self):
        return self.text

    """
    # This is incredibly slow right now
    @staticmethod
    def top_by_section(section,range=30,n=10):
        # Range is the number of days to look back for tags
        too_old = datetime.now() - timedelta(days = range)
        tags = Tag.objects.all() \
                .filter(content__section=section) \
                .filter(content__issue__issue_date__gt = too_old) \
                .annotate(content_count=Count('content')) \
                .order_by('-content_count')[:n]
        return tags
    """

    def get_absolute_url(self):
        return '/tag/%s' % urlname(self.text)

    @property
    def rss_url(self):
        return '/feeds/tag/%s' % urlname(self.text)


def contrib_pic_path(instance, filename):
    ext = splitext(filename)[1]
    name = '%s_%s_%s' % \
        (instance.first_name, instance.middle_name, instance.last_name)
    return 'photos/contrib_pics/' + name + ext


class Contributor(models.Model):
    """
    Someone who contributes to the Crimson,
    like a staff writer, a photographer, or a guest writer.

    # Create a contributor
    >>> c = Contributor(first_name='Dan', middle_name='C',last_name='Carroll')

    # Test the unicode string
    >>> str(c)
    'Dan C. Carroll'

    # Default is active
    >>> c.is_active
    True
    """

    first_name = models.CharField(blank=False, null=True, max_length=70)
    last_name = models.CharField(blank=False, null=True, max_length=100)
    middle_name = models.CharField(blank=True, null=True, max_length=70)
    # NOTE: this actually gets updated when published
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(
        default=True, db_index=True,
        help_text='This should be true for anyone who could possibly still '
                  'write for The Crimson, including guest writers.')
    bio_text = models.CharField(
        blank=True, max_length=500, null=True,
        help_text='Short biographical blurb about yourself, less than 500 '
                  'characters.')
    image = models.ImageField(
        upload_to=contrib_pic_path, blank=True, null=True,
        help_text='This should be a profile picture.')
    twitter = models.CharField(
        blank=True, null=True, max_length=70,
        help_text='Your username without the @ sign.')
    email = models.CharField(
        blank=True, null=True, max_length=70,
        help_text='In the form of email@thecrimson.com.')
    searchable = models.BooleanField(
        blank=False, default=True, db_index=True,
        help_text="Allow search engines to index this contributor's profile.")

    GENDER_CHOICES = (
        ('f', 'Female'),
        ('m', 'Male'),
        ('other', 'Other'),
    )

    gender = models.CharField(
        blank=True, null=True, default='other', max_length=70,
        choices=GENDER_CHOICES,
        help_text='Important for generating article taglines correctly.')

    TITLE_CHOICES = (
        ('cstaff', 'Crimson staff writer'),
        ('contrib', 'Contributing writer'),
        ('photog', 'Photographer'),
        ('design', 'Designer'),
        ('editor', 'Editor'),
        ('opinion', 'Crimson opinion writer'),
        ('opinion_contrib', 'Contributing opinion writer'),
    )

    # user inputted title - can be null, which triggers automatic
    # generation of actual title property
    _title = models.CharField(
        blank=True, null=True, max_length=70, choices=TITLE_CHOICES,
        verbose_name='title')

    # returns user inputted title or generates a default
    @property
    def title(self):
        TITLE_CHOICES_MAP = dict(self.TITLE_CHOICES)

        if self._title:
            return TITLE_CHOICES_MAP[self._title]
        # generate default title
        else:
            try:
                # TODO: change to .first() after switch to Django 1.7
                article_set = Article.objects.filter(
                    contributors=self).order_by('-created_on')[:1]

                if len(article_set) == 0:
                    return 'Contributor'

                # use their most recent byline_type
                return TITLE_CHOICES_MAP[article_set[0].byline_type]
            except (AttributeError, KeyError):
                # if they wrote articles, but didn't provide a byline
                return 'Writer'

    class Meta:
        ordering = ('last_name',)
        permissions = (
            ('contributor.can_merge', 'Can merge contributor profiles'),
        )

    def __unicode__(self):
        if self.middle_name is None or self.middle_name == '':
            m = ''
        else:
            m = ' ' + self.middle_name
        return '%s%s %s' % (self.first_name, m, self.last_name)

    @permalink
    def get_absolute_url(self):
        return (
            'content_writer_profile',
            [str(self.id), self.first_name, self.middle_name, self.last_name])
    get_absolute_url = ret_on_fail(get_absolute_url, '')

    @property
    def rss_url(self):
        return '/feeds/writer/%s' % str(self.id)

    def pic_display_url(self, size_spec):
        width, height = size_spec_to_size(
            size_spec, self.image.width, self.image.height)

        if width >= self.image.width and height >= self.image.height:
            return self.image.url

        grad_data = {'grad': False}
        if 'GRAD' in size_spec:
            grad_specs = size_spec[size_spec.index('GRAD') + 1:]
            grad_data = {
                'grad': True,
                'color': grad_specs[0],
                'max_opacity': grad_specs[1],
                'min_opacity': grad_specs[2],
                'direction': grad_specs[3]
            }
        options = {'size': (width, height), 'crop': 'smart', 'upscale': True}
        options = dict(options.items() + grad_data.items())
        return get_thumbnailer(self.image).get_thumbnail(options).url

    @property
    def bio(self):
        if self.bio_text and self.bio_text.strip() != '':
            return self.bio_text
        else:
            return ''

    def get_tagline(self, byline_type=None):
        # grab the titles of the authors
        if byline_type:
            title = dict(self.TITLE_CHOICES)[byline_type]
        else:
            title = self.title

        tagline = ''

        # if the contributor has neither email nor twitter, don't
        # generate tagline
        if not (self.email or self.twitter):
            return ''
        # otherwise generate the tagline
        if self.email:
            tagline += '%s %s can be reached at %s.' % (
                title, self, self.email)
            if self.twitter:
                pronoun = 'them'
                if self.gender == 'm':
                    pronoun = 'him'
                elif self.gender == 'f':
                    pronoun = 'her'
                tagline += ' Follow %s on Twitter <a href="https://www.' \
                           'twitter.com/%s" target=_blank>@%s</a>.' % (
                               pronoun, self.twitter, self.twitter)
        else:
            tagline += ('Follow %s %s on Twitter <a href="https://www.twitter'
                        '.com/%s" target=_blank>@%s</a>.'
                        % (title.lower(), self, self.twitter, self.twitter))

        return tagline


class SectionLayoutInstance(models.Model):
    active = models.BooleanField(default=False)
    section = models.ForeignKey('Section')
    layoutinstance = models.ForeignKey('placeholders.LayoutInstance')

    class Meta:
        # Trick South into using the original auto-generated M2M tables
        auto_created = 'Section'
        db_table = 'content_section_layout_instances'


class SectionManager(models.Manager):
    def get_queryset(self):
        return super(SectionManager, self).get_queryset() \
                                          .filter(can_have_articles=True)


class Section(models.Model):
    name = models.CharField(blank=False, max_length=50, db_index=True)
    can_have_articles = models.BooleanField(
        default=True,
        help_text='Whether articles can belong to this section')
    audiodizer_id = models.IntegerField(blank=True, null=True)
    layout_instances = models.ManyToManyField(
        'placeholders.LayoutInstance',
        through=SectionLayoutInstance, blank=False, default=None)

    objects = SectionManager()
    all_objects = models.Manager()

    @staticmethod
    def cached(section_name=None):
        a = cache.get('sections_cached')
        if a is None:
            a = dict([(s.slug(), s) for s in Section.all_objects.all()])
            cache.set('sections_cached', a, 1000000)
        if section_name:
            return a[section_name]
        return a

    """
    def top_tags(self,range=30,n=10):
        return Tag.top_by_section(self,range)
    """

    @permalink
    def get_absolute_url(self):
        return ('content.section.%s' % self.slug(), [])

    def slug(self):
        return self.name.lower().replace(':', '').replace(' ', '_')

    @property
    def layout(self):
        try:
            return self.layout_instances.filter(
                sectionlayoutinstance__active=True)[0]
        except IndexError:
            return None

    @property
    def rss_url(self):
        return '/feeds/section/%s' % self.name.lower()

    def __unicode__(self):
        return self.name


class IssueManager(models.Manager):
    LIVE = Q(web_publish_date__lte=datetime.now())
    DAILY = Q(special_issue_name='') | Q(special_issue_name=None)

    @property
    def live(self):
        return self.get_queryset().filter(IssueManager.LIVE)

    @property
    def special(self):
        return self.get_queryset().exclude(IssueManager.DAILY)

    @property
    def daily(self):
        return self.get_queryset().filter(IssueManager.DAILY)

    @property
    def live_daily(self):
        return self.daily.filter(IssueManager.LIVE)

    @property
    def live_special(self):
        return self.special.filter(IssueManager.LIVE)


class Issue(models.Model):
    """
    A set of content (articles, photos) for a particular date.

    Special issues should NEVER be displayed by default on the index.
    They should be displayed via content modules or special redirects.

    # Clear out the fixture preloaded issues
    >>> a = [i.delete() for i in Issue.objects.all()]

    # Create some issues
    >>> from datetime import datetime, timedelta
    >>> deltas = [timedelta(days=i) for i in range(-5, 6) if i]
    >>> now = datetime.now()
    >>> for d in deltas:
    ...     a = Issue.objects.create(issue_date=now+d)

    # make some of them special
    >>> i1 = Issue.objects.get(pk=1)
    >>> i1.special_issue_name = "Commencement 2008"
    >>> i1.save()
    >>> i2 = Issue.objects.get(pk=6)
    >>> i2.special_issue_name = "Election 2008"
    >>> i2.save()

    # managers
    >>> Issue.objects.all().count()
    10
    >>> Issue.objects.special.all().count()
    2
    >>> Issue.objects.daily.all().count()
    8
    >>> Issue.objects.live.all().count()
    5
    >>> Issue.objects.live_special.all().count()
    1
    >>> Issue.objects.live_daily.all().count()
    4

    # set_as_current and get_current
    >>> i3 = Issue.objects.get(pk=5)
    >>> i3.set_as_current()
    >>> assert Issue.get_current().issue_date, i2.issue_date
    """

    special_issue_name = models.CharField(
        blank=True, null=True,
        help_text='Leave this blank for daily issues!!!', max_length=100,
        db_index=True
    )
    web_publish_date = models.DateTimeField(
        null=True,
        blank=False, help_text='When this issue goes live (on the web).'
    )
    issue_date = models.DateField(
        blank=False, help_text='Corresponds with date of print edition.',
        db_index=True
    )
    fm_name = models.CharField(
        'FM name', blank=True, null=True, max_length=100,
        help_text='The name of the FM issue published on this issue date'
    )
    arts_name = models.CharField(
        blank=True, null=True, max_length=100,
        help_text='The name of the Arts issue published on this issue date'
    )
    comments = models.TextField(
        blank=True, null=True, help_text='Notes about this issue.'
    )

    objects = IssueManager()

    class Meta:
        ordering = ['-issue_date']

    @property
    def fm_cover(self):
        if not self.fm_name:
            return None
        s = Section.cached('fm')
        a = Article.objects.recent.filter(
            issue=self,
            rel_content__content_type=Image.content_type(), section=s) \
            .distinct()[:1]
        return a[0].main_rel_content if a else None

    @property
    def arts_cover(self):
        if not self.arts_name:
            return None
        s = Section.cached('arts')
        a = Article.objects.recent.filter(
            issue=self,
            rel_content__content_type=Image.content_type(), section=s) \
            .distinct()[:1]
        if a is not None:
            return a[0].main_rel_content
        else:
            return None

    @permalink
    def get_absolute_url(self):
        return (
            'content_index',
            [self.issue_date.year, self.issue_date.month, self.issue_date.day])

    @staticmethod
    def last_n(n, rece_date=None):
        """Last n issue, by date, only chooses issues >= rece_date"""
        if rece_date is None:
            rece_date = date.today()
        i = cache.get('last_%d_issues_%s' % (n, str(rece_date)))

        if i is None:
            i = Issue.objects.filter(issue_date__lte=rece_date)\
                             .order_by('-issue_date')[:n]
            cache.set('last_%d_issues_%s' % (n, str(rece_date)), i, 60 * 60)
        if len(i) == 0:
            raise Exception('There are no issues.')
        return i

    @staticmethod
    def get_current():
        """gets current issue from cache"""
        i = cache.get('current_issue')
        if not i:
            i = Issue.objects.latest('issue_date')
            i.set_as_current()
        return i

    def save(self, *args, **kwargs):
        # web publish date is 6 am on the issue date
        if self.web_publish_date is None:
            self.web_publish_date = datetime.combine(self.issue_date, time(6))
        return super(Issue, self).save(*args, **kwargs)

    def set_as_current(self, timeout=3600):
        return cache.set('current_issue', self, timeout)

    def __unicode__(self):
        if self.issue_date.year >= 1900:
            d = self.issue_date.strftime('%A, %B %d, %Y')
        else:
            d = strftime_safe(self.issue_date, '%A, %B %d, %Y')

        if (self.special_issue_name is not None and
                self.special_issue_name != ''):
            return '%s: %s' % (self.special_issue_name, d)
        else:
            return d


class ImageManager(ContentManager):
    def get_queryset(self):
        s = super(ImageManager, self).get_queryset()
        # this is a hella ghetto way to make sure image galleries always return
        # images in the right order.  this is probably really inefficient
        if self.__class__.__name__ == 'ManyRelatedManager':
            s = s.order_by('gallerymembership__order')
        return s


def image_get_save_path(instance, filename):
    ext = splitext(filename)[1]
    key = rand_str(10) if instance.pk is None else str(instance.pk)
    return datetime.now().strftime('photos/%Y/%m/%d/%H%M%S_') + key + ext


def download_upstream(file_field):
    logger.info('Downloading image ' + file_field.name + ' from upstream')
    dirpath = os.path.dirname(file_field.path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    response = urllib2.urlopen(settings.UPSTREAM_MEDIA_URL + file_field.name)
    raw_photo = response.read()
    with open(file_field.path, 'w') as f:
        f.write(raw_photo)


class Image(Content):

    """
    An image. Handles attributes about image. Handling of image resizing and
    cropping is done by display() and ImageSpec objects

    # TODO: not quite sure how to test Image

    """

    # standard image size constraints:
    #  width, height, crop_ratio ( 0 => not cropped )
    SIZE_TINY = (75, 75, 1, 1)
    SIZE_SMALL = (100, 100, 1, 1)
    SIZE_THUMB = (150, 150, 0, 0)
    SIZE_STAND = (635, 630, 0, 0)
    SIZE_LARGE = (900, 900, 0, 0)
    SIZE_FULL = (960, 0, 0, 0)

    # caption = models.CharField(blank=True, null=True, max_length=1000)
    # kicker = models.CharField(blank=True, null=True, max_length=500)
    # make sure pic is last: photo_save_path needs an instance, and if this
    #  attribute is processed first, all the instance attributes will be blank
    pic = models.ImageField(upload_to=image_get_save_path,
                            width_field='width',
                            height_field='height')
    # Data for crops.  We store the 1:1 ratio crop as the location of
    # its top left corner and the length of a side.
    crop_x = models.IntegerField(null=True)
    crop_y = models.IntegerField(null=True)
    crop_side = models.IntegerField(null=True)
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    is_archiveimage = models.BooleanField(default=False)

    objects = ImageManager()

    def __init__(self, *args, **kwargs):
        try:
            super(Image, self).__init__(*args, **kwargs)
        except IOError:
            if settings.DOWNLOAD_UPSTREAM_MEDIA:
                download_upstream(self.pic)
            else:
                raise
        if (settings.DOWNLOAD_UPSTREAM_MEDIA and
                not self.pic.storage.exists(self.pic.name)):
            download_upstream(self.pic)

    @property
    def img_title(self):
        """Title / alt for <img> tags."""
        return self.title

    @property
    def orientation(self):
        try:
            ratio = float(self.pic.width) / float(self.pic.height)
        # TODO figure out which exception is raised when self.pic can't
        # be found
        except:
            ratio = 1
        if ratio >= 1.4:
            return 'wide'
        else:
            return 'tall'

    def __getattr__(self, attr):
        'dispatches calls to standard sizes to display()'
        try:
            size = getattr(self.__class__, 'SIZE_%s' % attr.upper())
            return self.display(*size)
        except:
            return getattr(super(Image, self), attr)

    # Compatibility properties:
    @property
    def kicker(self):
        return self.title

    @kicker.setter
    def kicker(self, value):
        self.title = value

    @property
    def caption(self):
        return self.description

    @caption.setter
    def caption(self, value):
        self.description = value

    def display_url(self, size_spec):
        """ convenience method for the pic attribute's method of same name """
        try:
            width, height = size_spec_to_size(size_spec,
                                              self.width, self.height)
        except:
            if settings.DOWNLOAD_UPSTREAM_MEDIA:
                download_upstream(self.pic)
                width, height = size_spec_to_size(size_spec,
                                                  self.width, self.height)
            else:
                raise
        if width >= self.width and height >= self.height:
            return self.absolute_url()

        grad_data = {'grad': False}
        if 'GRAD' in size_spec:
            grad_specs = size_spec[size_spec.index('GRAD') + 1:]
            grad_data = {
                'grad': True,
                'color': grad_specs[0],
                'max_opacity': grad_specs[1],
                'min_opacity': grad_specs[2],
                'direction': grad_specs[3]
            }
        options = {'size': (width, height), 'crop': 'smart', 'upscale': True}
        options = dict(options.items() + grad_data.items())
        # We should fix the thumbnailer so that this can't raise an exception
        try:
            thumbnail_url = get_thumbnailer(
                self.pic).get_thumbnail(options).url
        except Exception:
            thumbnail_url = '%simages/error.png' % settings.STATIC_URL
        return thumbnail_url

    def absolute_url(self):
        """ convenience method for the pictures absolute url """
        return '%s%s' % (settings.MEDIA_URL, self.pic)

    def crop_thumb(self, size_spec, crop_coords):
        """ convenience method for the pic attribute's method of same name """
        self.crop_x = crop_coords[0]
        self.crop_y = crop_coords[1]
        self.crop_side = crop_coords[2] - crop_coords[0]
        self.pic.crop_thumb(size_spec, crop_coords)

    def delete_old_thumbs(self):
        """ convenience method for pic's attribute of same name"""
        self.pic.delete_old_thumbs()

    def __unicode__(self):
        return self.title

    def identifier(self):
        return make_url_friendly(self.title)

    def admin_thumb(self):
        """HTML for tiny thumbnail in the admin page."""
        if self.pic:
            return """<img src="%s">""" % self.display_url(Image.SIZE_TINY)
        return '(No picture)'
    admin_thumb.allow_tags = True


def pdf_get_save_path(instance, filename):
    ext = splitext(filename)[1]
    key = rand_str(10) if instance.pk is None else str(instance.pk)
    return datetime.now().strftime('pdf/%Y/%m/%d/') + key + ext


def pdf_thumb_get_save_path(instance, filename):
    ext = splitext(filename)[1]
    key = rand_str(10) if instance.pk is None else str(instance.pk)
    return datetime.now().strftime('pdf/thumbnails/%Y/%m/%d/') + \
        key + '-thumb' + ext


class PDF(Content):
    document = models.FileField(
        upload_to=pdf_get_save_path, verbose_name='PDF document')
    thumbnail = models.ImageField(
        upload_to=pdf_thumb_get_save_path, blank=True, null=True,
        verbose_name='PDF thumbnail')

    objects = ContentManager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'PDF'


def misc_get_save_path(instance, filename):
    ext = splitext(filename)[1]
    slug = make_file_friendly(instance.slug)
    return datetime.now().strftime('misc/%Y/%m/%d/%H%M%S_') + slug + ext


class Widget(Content):

    """
    A widget, such as a chart or graph in JS.

    """
    html = models.TextField(null=False)
    javascript = models.TextField(null=False)
    is_highcharts = models.BooleanField(null=False, default=False)
    is_d3 = models.BooleanField(null=False, default=False)
    pic = models.ImageField(upload_to=misc_get_save_path, blank=True)

    objects = ContentManager()

    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)

    def display_url(self, size_spec, upscale=False):
        if self.pic:
            width, height, _, _ = size_spec
            options = {'size': (width, height), 'crop': False, 'upscale': True}
            return get_thumbnailer(self.pic).get_thumbnail(options).url
        else:
            return ''

    @property
    def caption(self):
        return self.description

    def __unicode__(self):
        return self.title


class ExternalContent(Content):
    repr_type = models.ForeignKey(
        ContentType, blank=False,
        verbose_name='content type')
    redirect_url = models.CharField(
        max_length=100, blank=False,
        verbose_name='redirect URL')
    image = models.ForeignKey(
        Image, blank=True, null=True,
        verbose_name='associated image')

    objects = ContentManager()

    def _render(self, method, context=None, request=None, **kwargs):
        if 'ctype' not in kwargs:
            kwargs['ctype'] = self.repr_type
        return super(ExternalContent, self)._render(method, context, request,
                                                    **kwargs)

    def _render_to_response(self, method, context=None, request=None,
                            **kwargs):
        return HttpResponsePermanentRedirect(self.redirect_url)

    @property
    def headline(self):
        return self.title

    @property
    def subheadline(self):
        return self.subtitle

    @property
    def teaser(self):
        return self.description

    @property
    def kicker(self):
        return self.title

    @property
    def caption(self):
        return self.description

    @property
    def pic(self):
        return self.image

    def get_absolute_url(self):
        return self.redirect_url

    @property
    def main_rel_content(self):
        return self.image

    def rel_not_shortcoded(self):
        return [self.image]

    @property
    def main_rel_content_is_shortcoded(self):
        return False

    def rel_shortcoded(self):
        return []

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'external content'
        verbose_name_plural = verbose_name


class Gallery(Content):
    """
    A collection of displayed content (images, youtube, infographics, etc.)
    """

    # old_title = models.CharField(blank=False, null=False, max_length=200)
    # old_description = models.TextField(blank=False, null=False)
    contents = models.ManyToManyField(
        Content, through='GalleryMembership',
        related_name='galleries_set')
    layout_instance = models.ForeignKey(
        'placeholders.LayoutInstance',
        null=True, blank=True, default=None, on_delete=models.SET_NULL)
    objects = ContentManager()

    @property
    def img_title(self):
        """Title/alt for an <img> tag"""
        return self.title

    def display_url(self, size_spec, upscale=False):
        if self.cover_image is None:
            return ''
        return self.cover_image.display_url(size_spec)

    @property
    def cover_image(self):
        # TODO: clear this on save
        if not hasattr(self, '_cover_image'):
            if not self.contents.all():
                ci = None
            else:
                ci = self.contents.order_by('galleries_set')[0].child
            self._cover_image = ci
        return self._cover_image

    @property
    def main_rel_content(self):
        return self.cover_image

    @property
    def sorted_contents(self):
        # XXX This requires N + 1 queries, because whoever designed the
        # GalleryMembership class decided galleries could contain any
        # Content, not just Image. -_-
        acrs = GalleryMembership.objects.filter(gallery=self).prefetch_related(
            'content')
        return [x.content.child for x in acrs]

    @property
    def admin_contents(self):
        return self.sorted_contents

    @property
    def admin_content_pks(self):
        acrs = GalleryMembership.objects.filter(gallery=self)
        return ';'.join([str(x.content.pk) for x in acrs])

    def __unicode__(self):
        return self.title

    def delete(self):
        self.contents.clear()
        super(Gallery, self).delete()

    class Meta:
        verbose_name_plural = 'galleries'


class GalleryMembership(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='gallery_set')
    content = models.ForeignKey(Content, related_name='content_set')
    order = models.IntegerField()

    class Meta:
        ordering = ('order',)


def youtube_get_save_path(instance, filename):
    ext = splitext(filename)[1]
    filtered_capt = make_file_friendly(instance.slug)
    if filtered_capt == '':
        filtered_capt = make_file_friendly(instance.title)
    return datetime.now().strftime('photos/%Y/%m/%d/%H%M%S_') + \
        filtered_capt + ext


class Video(Content):
    """Embeddable YouTube video."""

    key = models.CharField(
        blank=False, null=False, max_length=100,
        help_text='youtube.com/watch?v=(XXXXXX)&... part of the YouTube URL. '
        'NOTE: THIS IS NOT THE ENTIRE YOUTUBE URL.',
        db_index=True)
    # old_title = models.CharField(blank=False, null=False, max_length=200)
    # old_description = models.TextField(blank=False, null=False)
    pic = models.ImageField(upload_to=youtube_get_save_path, null=True)

    objects = ContentManager()

    @property
    def img_title(self):
        """Title/alt for <img> tags."""
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'videos'

    def display_url(self, size_spec, upscale=False):
        if self.pic:
            width, height, _, _ = size_spec
            options = {'size': (width, height), 'crop': False, 'upscale': True}
            try:
                pic_url = get_thumbnailer(self.pic).get_thumbnail(options).url
            except InvalidImageFormatError:
                if settings.DOWNLOAD_UPSTREAM_MEDIA:
                    download_upstream(self.pic)
                    pic_url = get_thumbnailer(self.pic).get_thumbnail(
                        options).url
                else:
                    raise
            return pic_url
        else:
            return ''

    @property
    def main_rel_content(self):
        return self

    @property
    def youtube_url(self):
        return 'https://www.youtube.com/watch?v=%s' % self.key

    def admin_youtube(self):
        return '<a href="%s">%s</a>' % (self.youtube_url, self.youtube_url)
    admin_youtube.allow_tags = True
    admin_youtube.short_description = 'YouTube Link'

    def admin_thumb(self):
        """HTML for tiny thumbnail in the admin page."""
        if self.pic:
            return """<img src="%s">""" % self.display_url(Image.SIZE_TINY)
        else:
            return 'No Preview'
    admin_thumb.allow_tags = True
    admin_thumb.short_description = 'Thumbnail'


class FlashGraphic(Content):
    """A Flash Graphic."""

    graphic = models.FileField(
        upload_to=misc_get_save_path, null=False, blank=False)
    pic = models.ImageField(
        upload_to=misc_get_save_path, blank=False, null=False)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title

    objects = ContentManager()

    def display_url(self, size_spec, upscale=False):
        if self.pic:
            width, height, _, _ = size_spec
            options = {'size': (width, height), 'crop': False, 'upscale': True}
            return get_thumbnailer(self.pic).get_thumbnail(options).url
        else:
            return ''

    def admin_thumb(self):
        """HTML for tiny thumbnail in the admin page."""
        if self.pic:
            return """<img src="%s">""" % self.pic.display_url(Image.SIZE_TINY)
        else:
            return 'No Preview'
    admin_thumb.allow_tags = True
    admin_thumb.short_description = 'Thumbnail'


class Table(Content):
    """
    A table of data. Represents uploaded csv files in json format for easier
    parsing, but retains the original.
    """

    csv_file = models.FileField(
        upload_to=misc_get_save_path, null=False, blank=False)
    json_file = models.FileField(
        upload_to=misc_get_save_path, null=False, blank=False)

    objects = ContentManager()

    def update_json(self):
        # Open the csv if not already
        if self.csv_file.closed:
            self.csv_file.open()

        # Check in case the previous "open" failed
        if not self.csv_file.closed:
            # Read contents of CSV file
            # splitlines is used for universal newlines
            reader = csv.reader(self.csv_file.read().splitlines())
            # Default to empty table
            table_data = {'head': [], 'body': []}
            # Build up a list of rows
            row_num = 0
            for row in reader:
                if row_num == 0:
                    table_data['head'] = row
                else:
                    table_data['body'].append(row)
                row_num += 1
            # Serialize to json
            json_out = json.dumps(table_data)
            # Save file in the same location as the original CSV, with ".json"
            json_file_name = splitext(self.csv_file.name)[0] + '.json'
            # Save file. Use "False" to prevent recursive saving
            self.json_file.save(json_file_name, ContentFile(json_out), False)

    def __unicode__(self):
        return self.title


class Map(Content):
    """
    A Google Map Object
    """

    # values used by Google Maps API
    zoom_level = models.PositiveSmallIntegerField(default=15)
    center_lat = models.FloatField(default=42.373002)
    center_lng = models.FloatField(default=-71.11905)
    display_mode = models.CharField(default='Map', max_length=50)
    width = models.IntegerField(default='300')
    height = models.IntegerField(default='300')
    # display stuff
    # caption = models.CharField(blank=True, max_length=1000)

    # Compatibility property:
    @property
    def caption(self):
        return self.description

    @caption.setter
    def caption(self, value):
        self.description = value

    def __unicode__(self):
        return self.title

    objects = ContentManager()


class Marker(models.Model):
    """
    Markers for a Google Map
    """
    COLOR_CHOICES = (
        ('yellow', 'Yellow'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('ltblue', 'Light blue'),
        ('orange', 'Orange'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
        ('red', 'Red'),
    )

    map = models.ForeignKey(Map, related_name='markers')
    lat = models.FloatField(blank=False, db_index=True)
    lng = models.FloatField(blank=False, db_index=True)
    color = models.CharField(
        max_length=255, choices=COLOR_CHOICES,
        default='red')
    popup_text = models.CharField(
        blank=True, max_length=1000,
        help_text='text that appears when the user clicks the marker')

    @classmethod
    def valid_colors(cls):
        return [choice[0] for choice in cls.COLOR_CHOICES]

    @classmethod
    def default_color(cls):
        return cls._meta.get_field_by_name('color')[0].default

    def __unicode__(self):
        return str(self.map) + ' (' + str(self.lat) + ',' + str(self.lng) + ')'


class Article(Content):
    """
    Non serial text content

    # create some articles
    >>> c = Contributor.objects.create(first_name='Kristina',
    ...     last_name='Moore')
    >>> t = Tag.objects.create(text='tagg')
    >>> i = Issue.get_current()
    >>> s = Section.objects.create(name='movies')
    >>> a1 = Article.objects.create(headline='abc', text='abcdefg',
    ...     issue=i, section=s, proofer=c, sne=c)
    >>> a2 = Article.objects.create(headline='head line',
    ...     text='omg. lolz.', issue=i, section=s, proofer=c, sne=c)

    # teasers
    >>> str(a2.long_teaser)
    'omg. lolz.'

    """

    JUMP_REGEX = compile(r'(.*)<!--more-->', DOTALL)

    BYLINE_TYPE_CHOICES = (
        ('cstaff', 'Crimson Staff Writer'),
        ('contrib', 'Contributing Writer'),
        ('opinion', 'Crimson Opinion Writer'),
        ('opinion_contrib', 'Contributing Opinion Writer')
    )

    objects = ContentManager()

    # headline = models.CharField(blank=False, max_length=127, db_index=True)
    # subheadline = models.CharField(blank=True, null=True, max_length=255)
    byline_type = models.CharField(
        blank=True, null=True, max_length=70, choices=BYLINE_TYPE_CHOICES,
        help_text='This will automatically be pluralized if there '
                  'are multiple contributors.')
    text = models.TextField(blank=False, null=False)
    page = models.CharField(
        blank=True, null=True, max_length=10,
        help_text='Page in the print edition.')
    layout_instance = models.ForeignKey(
        'placeholders.LayoutInstance',
        null=True, blank=True, default=None, on_delete=models.SET_NULL)
    rel_content = models.ManyToManyField(
        Content,
        through='ArticleContentRelation', blank=True,
        related_name='rel_content')
    rec_articles = models.ManyToManyField('self', blank=True,
                                          symmetrical=False)
    parent_topic = models.ForeignKey('TopicPage', blank=True, null=True)

    tagline = models.BooleanField(
        blank=True, default=False,
        help_text='Auto-generate the tagline.')

    @property
    def rel_admin_content(self):
        acrs = ArticleContentRelation.objects.filter(article=self)
        return acrs

    @property
    def rec_articles_admin(self):
        return ';'.join([str(x.pk) for x in self.rec_articles.all()])

    @property
    def has_jump(self):
        return bool(self.JUMP_REGEX.search(self.text))

    @property
    def text_before_jump(self):
        match = self.JUMP_REGEX.search(self.text)
        if match:
            return match.group(1)
        else:
            return self.text.replace('<p>&nbsp;</p>', '')

    @property
    def snippet(self):
        """Returns teaser text or before-jump text; whichever is present"""
        return self.teaser or self.text_before_jump

    @property
    def groupless_headline(self):
        if self.group:
            group_name_pattern = '^' + re.escape(self.group.name) + ': '
            return re.sub(group_name_pattern, '', self.headline)
        return self.headline

    # Compatibility properties:
    @property
    def headline(self):
        return self.title

    @headline.setter
    def headline(self, value):
        self.title = value

    @property
    def subheadline(self):
        return self.subtitle

    @subheadline.setter
    def subheadline(self, value):
        self.subtitle = value

    @property
    def teaser(self):
        return self.description

    @teaser.setter
    def teaser(self, value):
        self.description = value

    # Override save to check whether we're modifying an existing article's text
    def save(self, *args, **kwargs):
        new_instance = True
        oldtext = ''
        if self.pk is not None:
            try:
                prev_article = Article.objects.get(pk=self.pk)
            except Article.DoesNotExist:
                prev_article = None

            if prev_article:
                new_instance = False
                oldtext = prev_article.text

                if int(prev_article.pub_status) is 1 and oldtext != self.text:
                    # If the text has changed, make a new Correction for
                    # the old text
                    corr = Correction(text=oldtext, article=self)
                    corr.save()

        super(Article, self).save(*args, **kwargs)

        # generate recommended articles for new non-empty articles
        if new_instance and len(self.text) > 0:
            if not self.rec_articles.all():
                if not self.keywords.all():
                    get_keywords_task.apply_async(
                        (self.pk,), link=generate_rec_articles_task.s())
                else:
                    generate_rec_articles_task.delay(self.pk)

    def delete(self):
        self.rel_content.clear()
        super(Article, self).delete()

    @property
    def long_teaser(self):
        return sub(r'<[^>]*?>', '', truncatewords(self.title, 50))

    @property
    def relation_content(self):
        rels = self.rel_content.all()
        relation_content = []
        # need to return child, so that subclass methods can be called
        for r in rels:
            try:
                r = r.child if r else None
            except IOError:
                logger.error('IOError in searching for main_rel_content!')

            if r is not None and not isinstance(r, Article):
                relation_content.append(r)

        return relation_content

    @property
    def main_rel_content(self):
        rels = self.rel_content.all()
        # need to return child, so that subclass methods can be called
        for r in rels:
            try:
                r = r.child if r else None
            except IOError:
                logger.error('IOError in searching for main_rel_content!')

            if r is not None and not isinstance(r, Article):
                return r

        return None

    @property
    def main_rel_content_is_shortcoded(self):
        main_acr = ArticleContentRelation.objects.filter(
            article=self, related_content=self.main_rel_content)[:1]
        return main_acr[0].shortcoded if main_acr else False

    def rel_not_shortcoded(self):
        """
        Gives you the traditionally related content minus all content
        that has been shortcoded in.
        """
        shortcoded_ids = self.rel_shortcoded()
        rel = list(self.rel_content.all())
        return [r for r in rel if r.child.id not in shortcoded_ids]

    def rel_shortcoded(self):
        """
        Unlike rel_not_shortcoded, this only looks at shortcoded content.
        It returns a list of all shortcoded content ids, regardless of whether
        or not it is traditionally related with an ArticleContentRelation.
        """
        return Article.extract_shortcoded_content(self.text)

    SHORTCODE_REGEX = compile(r'\{(.*?)\}')
    SHORTCODE_INSIDE_REGEX = compile(
        r'(image|video|flashgraphic|map|gallery|widget).*id=\"?(\d+)\"?')

    @staticmethod
    def extract_shortcoded_content(text):
        shortcoded_ids = []
        for match in Article.SHORTCODE_REGEX.findall(text):
            clean_match = strip_tags(match)
            try:
                search = Article.SHORTCODE_INSIDE_REGEX.findall(clean_match)
                if len(search) > 0:
                    found_id = int(search[0][1])
                    shortcoded_ids.append(found_id)
            except:
                print('Non-content/invalid shortcode found while '
                      'accumulating content!')
        return shortcoded_ids

    def __unicode__(self):
        return self.headline

    def identifier(self):
        return self.headline


class ArticleContentRelation(models.Model):
    article = models.ForeignKey(Article, related_name='ar')
    related_content = models.ForeignKey(Content)
    order = models.IntegerField(blank=True, null=True)
    shortcoded = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = ('order',)

    """
    class Meta:
        unique_together = (
            ('article', 'related_content',),
            ('article', 'order',)
    )
    """


class Word(models.Model):
    """
    Word in an Article's text. The objects in this table store the
    number of articles in which a given word appears in the last
    year (limited to words used in the last year). It is updated
    with a cron job fairly regularly.
    """
    word = models.CharField(db_index=True, max_length=150)
    last_updated = models.DateTimeField(auto_now_add=True, db_index=True)
    word_frequency = models.IntegerField(default=0)


class Keyword(models.Model):
    """
    Important word in an Article's text.
    """
    word = models.CharField(db_index=True, max_length=150, unique=True)
    articles = models.ManyToManyField(
        Article, related_name='keywords', through='ArticleKeywordRelation')

    def __unicode__(self):
        return self.word


class ArticleKeywordRelation(models.Model):
    article = models.ForeignKey(Article)
    keyword = models.ForeignKey(Keyword)
    score = models.FloatField(default=0)  # tf-idf word relevance score

    def __unicode__(self):
        return u'%s, %s' % (self.article.title, self.keyword.word)


class Review(models.Model):
    TYPE_CHOICES = (
        ('movie', 'Movie'),
        ('music', 'Music'),
        ('book', 'Book'),
    )
    RATINGS_CHOIES = tuple([(i, str(i)) for i in range(1, 6)])
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATINGS_CHOIES, db_index=True)
    article = models.ForeignKey(Article, null=True, blank=True)


class Score(models.Model):
    article = models.ForeignKey(Article, related_name='sports_scores')
    sport = models.ForeignKey(Tag, limit_choices_to={'category': 'sports'},)
    opponent = models.CharField(max_length=50, null=True, blank=True)
    our_score = models.CharField(max_length=20, null=True, blank=True)
    their_score = models.CharField(max_length=20, null=True, blank=True)
    home_game = models.BooleanField(default=True)
    text = models.CharField(max_length=50, null=True, blank=True)
    event_date = models.DateField()

    def __unicode__(self):
        if self.text:
            return self.text
        elif self.opponent and self.home_game:
            return 'Harvard %s %s %s' % (
                self.our_score, self.opponent, self.their_score)
        elif self.opponent and self.home_game:
            return '%s %s Harvard %s' % (
                self.opponent, self.their_score, self.our_score)


class Correction(models.Model):
    text = models.TextField(blank=False, null=False)
    dt = models.DateTimeField(auto_now=True, db_index=True)
    article = models.ForeignKey(Article, null=False, blank=False)

    def save(self, *args, **kwargs):
        return super(Correction, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.id)


def genericfile_get_save_path(instance, filename):
    ext = splitext(filename)[1]
    title = make_file_friendly(instance.title)
    return datetime.now().strftime('misc/genfiles/%Y/') + title + ext


class GenericFile(models.Model):
    """A Generic File (pdf/random thing on a form/etc.)."""

    gen_file = models.FileField(
        upload_to=genericfile_get_save_path, null=False, blank=False,
        verbose_name='File')
    title = models.CharField(blank=False, null=False, max_length=200)
    description = models.TextField(blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return self.title


class MostReadArticles(models.Model):
    """
    This has been repurposed to track both articles and topic pages.
    """
    create_date = models.DateTimeField(auto_now=True)
    article1 = models.ForeignKey(
        Content, null=False, blank=False, related_name='MostReadArticle1')
    article2 = models.ForeignKey(
        Content, null=False, blank=False, related_name='MostReadArticle2')
    article3 = models.ForeignKey(
        Content, null=False, blank=False, related_name='MostReadArticle3')
    article4 = models.ForeignKey(
        Content, null=False, blank=False, related_name='MostReadArticle4')
    article5 = models.ForeignKey(
        Content, null=False, blank=False, related_name='MostReadArticle5')
    key = models.CharField(blank=False, null=False, max_length=20)

    def articles(self):
        content = [self.article1, self.article2,
                   self.article3, self.article4,
                   self.article5]
        ret = []
        # Make sure that we are accessing the correct model.
        # If c is an article, c.article gets the article object
        # If c is a topic page, c.topicpage gets the topicpage object
        # getattr is the general way of doing this
        for c in content:
            ret.append(c.child)

        return ret


def package_pic_path(instance, filename):
    ext = splitext(filename)[1]
    title = instance.title.replace(' ', '')

    name = '%s' % \
        (title)
    return 'photos/' + name + ext


class TopicManager(ContentManager):
    def get(self, *args, **kwargs):
        if 'slug_path' in kwargs:
            slugs = kwargs['slug_path'].split('/')
            cur = None
            for s in slugs:
                cur = super(TopicManager, self).get(parent=cur, slug=s)
            return cur
        else:
            return super(TopicManager, self).get(*args, **kwargs)


class TopicPage(Content):
    objects = TopicManager()

    layout_instance = models.ForeignKey(
        'placeholders.LayoutInstance', null=True, blank=True, default=None,
        on_delete=models.SET_NULL)
    parent = models.ForeignKey(
        'content.TopicPage', null=True, blank=True, related_name='children')
    pos = models.IntegerField(
        null=False, default=0, blank=True,
        verbose_name='Position (only useful if there is a parent topic)')
    image = models.ForeignKey(
        Image, blank=True, null=True, verbose_name='Associated Image')

    def get_default_layout(self):
        from crimsononline.placeholders.models import Layout
        return Layout.objects.all()[0]

    def get_slug_path(self):
        slugs = []
        cur = self
        while cur is not None:
            slugs.insert(0, cur.slug)
            cur = cur.parent
        return '/'.join(slugs)

    @property
    def main_rel_content(self):
        return self.image

    @property
    def headline(self):
        return self.title

    @property
    def teaser(self):
        return mark_safe(self.description)

    def get_ordered_children(self):
        return self.children.order_by('pos')

    def get_all_ordered_children(self):
        return TopicPage.objects.admin_objects() \
            .filter(parent=self).order_by('pos')

    def __unicode__(self):
        return unicode(self.title + ' ' + self.subtitle)


class FeaturePackage(models.Model):

    PUB_CHOICES = (
        (0, 'Draft'),
        (1, 'Published'),
        (-1, 'Deleted'),
    )

    title = models.CharField(blank=False, null=False, max_length=250)

    description = models.TextField(blank=False, null=False)

    pub_status = models.IntegerField(
        null=False, choices=PUB_CHOICES,
        default=0, db_index=True)

    create_date = models.DateTimeField(auto_now_add=True)

    edit_date = models.DateTimeField(auto_now=True)

    # indicates where or not a big banner should appear on the index page
    feature = models.BooleanField(default=False)

    slug = models.CharField(blank=True, null=False, max_length=250)

    banner = models.ImageField(
        blank=True, null=True,
        upload_to=package_pic_path)

    class Meta:
        permissions = (
            ('content.can_publish', 'Can publish content',),
            ('content.can_unpublish', 'Can unpublish content',),
            ('content.can_delete_published', 'Can delete published content'),
        )


class FeaturePackageSection(models.Model):

    PUB_CHOICES = (
        (0, 'Draft'),
        (1, 'Published'),
        (-1, 'Deleted'),
    )

    title = models.CharField(blank=False, null=False, max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    icon = models.ImageField(blank=True, null=True, upload_to=package_pic_path)
    pub_status = models.IntegerField(
        null=False, choices=PUB_CHOICES,
        default=0, db_index=True)

    layout = models.ForeignKey(
        'placeholders.Layout', null=True, blank=True, default=None)
    slug = models.CharField(blank=True, null=False, max_length=250)
    MainPackage = models.ForeignKey(
        FeaturePackage, null=False, blank=False, related_name='sections')

    # Only here as a vestige from before the days of Placehoders app so we
    # don't forget which articles were associated with which
    # FeaturePackageSections - don't use these if you're making new
    # FeaturePackageSections.  Use Layouts!
    related_contents = models.ManyToManyField(
        Content, related_name='related_contents',
        through='PackageSectionContentRelation')

    @property
    def rel_admin_content(self):
        acrs = PackageSectionContentRelation.objects.filter(
            FeaturePackageSection=self)
        return ';'.join([str(x.related_content.pk) for x in acrs])

    class Meta:
        permissions = (
            ('content.can_publish', 'Can publish content',),
            ('content.can_unpublish', 'Can unpublish content',),
            ('content.can_delete_published', 'Can delete published content'),
        )


class PackageSectionContentRelation(models.Model):
    FeaturePackageSection = models.ForeignKey(
        FeaturePackageSection, related_name='fps')
    related_content = models.ForeignKey(Content)
    order = models.IntegerField(blank=True, null=True)
    isFeatured = models.BooleanField(default=False)

    class Meta:
        ordering = ('order',)


class BreakingNews(SingletonModel):
    title = models.CharField(
        blank=True, default='Breaking News', max_length=50)
    text = models.CharField(blank=True, max_length=250)
    link = models.URLField(blank=True, max_length=250)
    updated = models.TimeField(blank=True, null=True)
    enabled = models.BooleanField(default=False)

    modified_on = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.enabled and not(self.text):
            raise ValidationError('Must include text and time updated.')

    def save(self, *args, **kwargs):
        expire_all()
        return super(BreakingNews, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'Breaking news bar'

    class Meta:
        verbose_name = 'breaking news bar'
        verbose_name_plural = verbose_name


class IndexLayoutInstance(models.Model):
    active = models.BooleanField(default=False)
    index = models.ForeignKey('Index')
    layoutinstance = models.ForeignKey('placeholders.LayoutInstance')

    class Meta:
        # Trick South into using the original auto-generated M2M tables
        auto_created = 'Index'
        db_table = 'content_index_layout_instances'


class Index(SingletonModel):
    # home page singleton model
    # pretty bare, but we'll start with some layoutInstances

    layout_instances = models.ManyToManyField(
        'placeholders.LayoutInstance',
        blank=False, default=None, through=IndexLayoutInstance)

    @property
    def layout(self):
        try:
            return self.layout_instances.filter(
                indexlayoutinstance__active=True)[0]
        except IndexError:
            return None

    def __unicode__(self):
        return u'The Home Page'

    class Meta:
        verbose_name_plural = 'index'
