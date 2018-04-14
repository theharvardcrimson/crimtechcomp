from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib.sitemaps import FlatPageSitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView, TemplateView

from crimsononline.content import feeds, views
from crimsononline.content.sitemaps import ArticleSitemap
from crimsononline.servestatic import ServeDocsView

FILTER_URL_RE = r'(sections/(?P<sections>[\w,-]+)/)?' \
    '(types/(?P<types>[\w,-]+)/)?(page/(?P<page>\d+)/)?'


urlpatterns = []
"""
urlpatterns += [url(r'^todays-paper/', views.todays_paper)]
urlpatterns += patterns(
    '',
    url(r'^docs/(?P<path>.*)', ServeDocsView.as_view()),
    url(r'^search/', include('crimsononline.search.urls')),
    url(r'^select2/', include('django_select2.urls')),
)

# march madness (needs to be above new topic urls)
urlpatterns += patterns(
    'crimsononline.march_madness.views',
    url(r'^topic/2014/3/16/march-madness/$', 'index'),
)

urlpatterns += patterns(
    'crimsononline.content.views',
    url(r'writer/(?P<pk>\d+)/(?P<f_name>[\w\-\'\.\s]+)_'
        r'(?P<m_name>[\w\-\'\.\s]*)_(?P<l_name>[\w\-\'\.\s]+)/%s$' %
        FILTER_URL_RE,
        'writer', name='content_writer_profile'),
    url(r'^tag/(?P<tagname>[-\'a-zA-Z0-9 ]*)/%s$' % FILTER_URL_RE, 'tag',
        name='tagpage'),
    url(r'^section/', include('crimsononline.content.section_urls'),
        name='content_section'),
    url(r'^columns/(?P<section_name>[\w\s]+)?/?$', 'columns'),
    url(r'^$', 'index', name='content_index'),

    url(r'^topic/(?P<slug_path>[0-9\w_\-%/]+)/$', 'topic_page',
        name='content_topic'),
    url(r'^watermark/(?P<imageid>[0-9\w_\-%/]+)/$', 'image_watermark'),
    url(r'^classifieds/$',
        TemplateView.as_view(template_name='classifieds.html')),
    url(r'^jobbox/$', TemplateView.as_view(template_name='jobbox.html')),
    url(r'^interstitial_store/$',
        TemplateView.as_view(template_name='forms/interstitial_store.html')),
    url(r'^interstitials/ad_600x500/$',
        TemplateView.as_view(template_name='ad_600x500.html')),
    url(r'^interstitials/message/$',
        TemplateView.as_view(template_name='interstitial_message.html')),

    # redirects old urls
    url(r'article\.aspx$', 'redirect_article_aspx'),
    url(r'^writer\.aspx$', 'redirect_writer_aspx'),
    url(r'^info/comp\.aspx$', RedirectView.as_view(url='/about/')),

    # will be fixed with placeholders

    url(r'^feature/concussions/$',
        TemplateView.as_view(template_name='feature.html')),
    url(r'^article/2013/4/4/concussions-feature/$',
        RedirectView.as_view(url='/feature/concussions/')),
    url(r'^article/2013/5/28/commencement-2013-50th-reunion/$',
        RedirectView.as_view(
            url='/feature/commencement-2013/1963-reunion-issue/')),
    url(r'^article/2013/5/30/the-rise-of-hpac/$',
        RedirectView.as_view(
            url='/features/hpac/')),
    url(r'^article/2013/5/30/harvard-strong-boston-skyline/$',
        RedirectView.as_view(
            url='/features/marathon/')),
    url(r'^article/2013/9/8/freshman-survey-interactive-2017/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2013/frosh-survey/')),
    url(r'^article/2013/9/20/piecing-cambridge-together/$',
        RedirectView.as_view(
            url='/section/fm')),
    url(r'^article/2013/10/3/engineering-mike-smith/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2013/smith/')),
    url(r'^article/2013/10/17/lost-and-found-arts-cover/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2013/lost-and-found/')),
    url(r'^article/2013/10/24/hacking-harvard-cyberwar-huit/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2013/hackers/')),
    url(r'^article/2013/11/4/cambridge-city-council-election/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2013/city-council-election/')),
    url(r'^article/2013/11/21/academy-athletics-tradeoffs/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2013/other-field-study/')),
    url(r'^article/2013/11/22/jfk-assassination-50-years/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2013/jfk-50/')),
    url(r'^article/2013/12/31/top-news-stories-2013/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2013/top-stories/')),
    url(r'^article/2014/2/14/fifteen-hottest-2017/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2014/fifteen-hottest/')),
    url(r'^article/2014/3/6/flyby-housing-market-2014/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2014/housing-market/')),
    url(r'^article/2014/3/13/recruiting-basketball-dynasty/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2014/recruiting/')),
    url(r'^article/2014/4/24/harvard-alumni-donations/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2014/year-in-review/article/'
                'funny-alums/')),
    url(r'^article/2014/4/24/after-acceptance-first-generat/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2014/year-in-review/article/'
                'after-acceptance/')),
    url(r'^article/2014/4/24/2048-2014-venn-diagram/$',
        RedirectView.as_view(
            url='http://features.thecrimson.com/2014/year-in-review/')),

    url(r'^image/2013/10/16/lowchart-university-dean-college/$',
        RedirectView.as_view(
            url='http://static.thecrimson.com/pdf/college_dean_flowchart.pdf')
        ),
    url(r'^image/2013/10/23/endowment-infographic-final/$',
        RedirectView.as_view(
            url='http://static.thecrimson.com/extras/2013/endowment/'
                'index.html')
        ),
    url(r'^image/2013/12/17/kim-affidavit/$',
        RedirectView.as_view(
            url='http://static.thecrimson.com/extras/2013/kim_affidavit.pdf')
        ),
    url(r'^image/2014/1/29/honor-code-draft/$',
        RedirectView.as_view(
            url='http://static.thecrimson.com/extras/2014/'
                'honor-code-draft.pdf')
        ),

    url(r'^feature/(?P<title>[0-9\w_\-%]+)/(?P<sectionTitle>[0-9\w_\-%]+)/$',
        'feature_view', name='feature_package'),
    url(r'^feature/(?P<title>[0-9\w_\-%]+)/$', 'feature_view',
        name='feature_package'),
    url(r'^alerts/$',
        RedirectView.as_view(
            url='https://theharvardcrimson.wufoo.com/forms/'
                'get-harvard-breaking-news-alerts/')),

    url(r'^admissions/' + settings.CONTENT_URL_RE, 'get_content',
        name='content_admissions'),
    url(r'^admissions/((?P<page>\d+)/)?$', 'section_admissions',
        name='content.section.admissions'),

    # totally not flyby
    #url(r'^flyby/' + settings.CONTENT_URL_RE, 'get_content',
    #    name='content_flyby'),
    #url('^flyby/' + settings.CGROUP_URL_RE + settings.CONTENT_URL_RE,
    #    'get_grouped_content',
    #    name='flyby_content_grouped_content'),
    #url('^flyby/' + settings.CGROUP_URL_RE + settings.CGROUP_FILTER_URL_RE +
    #    '$',
    #    'get_content_group',
    #    name='flyby_content_contentgroup'),
    #url(r'^flyby/series/$', 'section_flyby_series'),
    #url(r'^flyby/today/$',
    #    TemplateView.as_view(template_name='flyby/harvard_today.html')),
    #url(r'^flyby/search/$',
    #    TemplateView.as_view(template_name='flyby/search.html')),
    #url(r'^flyby/' + settings.CGROUP_FILTER_URL_RE + '$', 'section_flyby',
    #    name='content.section.flyby'),

    # sponcon1
    url(r'^sponsored/$', 'section_sponsored', name='content.section.sponsored'),
    url(r'^sponsored/the-crimson-brand-studio/$',
        'section_sponsored',
        name='content.section.sponsored'),
    url(r'^sponsored/' + settings.SPONSORED_CONTENT_URL_RE,
        'get_sponsored_content',
        name='content_sponsored'),
)

urlpatterns += patterns(
    'crimsononline.archive_photos.views',
    url(r'^photoarchiver/$', 'upload_view', name='photoarchiver'),
)

# rss feed urls
urlpatterns += patterns(
    '',
    url(r'^feeds/writer/(?P<pk>\d+)/$',
        cache_page(settings.CACHE_STANDARD)(feeds.AuthorFeed())),
    url(r'^feeds/tag/(?P<tagname>[-\'a-zA-Z0-9 ]*)/$',
        cache_page(settings.CACHE_STANDARD)(feeds.TagFeed())),
    url(r'^feeds/section/features/$',
        cache_page(settings.CACHE_STANDARD)(feeds.FeatureFeed())),
    url(r'^feeds/section/(?P<section>[\w\-\'\.\s]*)/$',
        cache_page(settings.CACHE_STANDARD)(feeds.SectionFeed())),
    url(r'^feeds/full/section/(?P<section>[\w\-\'\.\s]*)/$',
        cache_page(settings.CACHE_STANDARD)(feeds.FullSectionFeed())),
)

sitemaps = {
    'flatpages': FlatPageSitemap,
    'articles': ArticleSitemap,
}

urlpatterns += patterns(
    '',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index',
        {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    url(r'^sitemap/contributors/$',
        'crimsononline.content.views.sitemap_contributors'),
    url(r'^sitemap/contributors/page/(\d+)/$',
        'crimsononline.content.views.sitemap_contributors'),
    url(r'^sitemap/$',
        'crimsononline.content.views.sitemap'),
    url(r'^sitemap/(\d{4})/$',
        'crimsononline.content.views.sitemap'),
    url(r'^sitemap/(\d{4})/(\d+)/$',
        'crimsononline.content.views.sitemap'),
)

urlpatterns += patterns(
    'crimsononline.ads.views',
    url(r'^ajax/is_local/', 'is_local', name='check_local'),
)

# special stuff

urlpatterns += patterns(
    '',
    url(r'^admin/', include('crimsononline.admin_cust.urls')),
    # required for python-social-auth login
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('crimsononline.newsletter.urls')),
)


# general articles
# THE MOST IMPORTANT SHIT

generic_patterns = patterns(
    'crimsononline.content.views',
    url('^' + settings.CONTENT_URL_RE, 'get_content', name='content_content'),
    url('^' + settings.CGROUP_URL_RE + settings.CONTENT_URL_RE,
        'get_grouped_content',
        name='content_grouped_content'),
    url('^' + settings.CGROUP_URL_RE + settings.CGROUP_FILTER_URL_RE + '$',
        'get_content_group',
        name='content_contentgroup'),
)

# ***********************************

urlpatterns += generic_patterns

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns(
    '',
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                               content_type='text/plain')),
)

urlpatterns += patterns(
    '',
    url(r'^ads\.txt$', TemplateView.as_view(template_name='ads.txt',
                                            content_type='text/plain')),
)

urlpatterns += patterns(
    '',
    url(r'^redactor/', include('redactor.urls')),
)

urlpatterns += patterns(
    'crimsononline.imageuploader.views',
    url(r'^imageupload/?$', 'image_upload_form'),
    url(r'^imageuploadtarget/?$', 'image_upload_target'),
    url(r'^imageuploadsubmit/?$', 'image_metadata_submit'),
)
"""
generic_patterns = patterns(
    'crimsononline.content.views',
    url('^' + settings.CONTENT_URL_RE, 'get_content', name='content_content'),
    url('^' + settings.CGROUP_URL_RE + settings.CONTENT_URL_RE,
        'get_grouped_content',
        name='content_grouped_content'),
    url('^' + settings.CGROUP_URL_RE + settings.CGROUP_FILTER_URL_RE + '$',
        'get_content_group',
        name='content_contentgroup'),
)