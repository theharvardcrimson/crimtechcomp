import datetime
import re
from collections import defaultdict

from django.conf import settings
from django.core.management.base import NoArgsCommand

from apiclient.discovery import build
from httplib2 import Http
from oauth2client.client import SignedJwtAssertionCredentials

from crimsononline.content.generators import cache_homepage
from crimsononline.content.models import (
    Article, ExternalContent, MostReadArticles, TopicPage)

# Column indices. UNIQUE_PAGEVIEWS = 2, TIME_ON_PAGE = 3, etc.
PAGE_URL = 0
PAGEVIEWS = 1


class Command(NoArgsCommand):
    help = 'This command will create a new most read article row'

    SOURCE_APP = 'thecrimson.com'

    END_DATE = datetime.datetime.now()
    START_DATE = END_DATE - datetime.timedelta(days=2)

    # These are the columns numbers for the rows returned by the Google
    # Analytics query. A row will look like
    # [url, pageviews, uniquePageviews, timeOnPage, bounces, ...]
    METRICS = ['ga:pageviews', 'ga:uniquePageviews', 'ga:timeOnPage',
               'ga:bounces', 'ga:entrances', 'ga:exits']

    DEFAULT_QUERY_OPTIONS = {
        'ids': 'ga:509545',
        'start_date': START_DATE.strftime('%Y-%m-%d'),
        'end_date': END_DATE.strftime('%Y-%m-%d'),
        'dimensions': 'ga:pagePath',
        'metrics': ','.join(METRICS),
        'sort': '-ga:pageviews',
        'max_results': '15'
    }

    KEY_FILTERS = {
        # starts with /article, is not a random page of the article (we only
        # count landing page)
        'content': 'ga:pagePath!~^.*?page=([1-9]+|single)$',
        'admissions': 'ga:pagePath=~/admissions/article/',
        'flyby': 'ga:pagePath=~/flyby/article/'
    }

    def slug_from_page_path(self, page_path):
        end = page_path.rfind('/')
        start = page_path.rfind('/', 0, end) + 1
        return page_path[start:end]

    date_regex = re.compile('.*/article/(\d{4})/(\d{1,2})/(\d{1,2})/.*')

    def date_from_page_path(self, page_path):
        reg = self.date_regex.match(page_path)
        try:
            return datetime.datetime(year=int(reg.groups()[0]),
                                     month=int(reg.groups()[1]),
                                     day=int(reg.groups()[2]))
        except:
            return None

    def handle_noargs(self, **options):
        """
        Generate the most read articles objects. This is run every 15 minutes
        by an external cron job.

        Grab the most visited urls from Google Analytics, find the
        corresponding content, and save them as a MostReadArticles object.
        """

        # Authorize an http object with our stored credentials
        credentials = SignedJwtAssertionCredentials(
            settings.ANALYTICS_CONFIG['client_email'],
            settings.ANALYTICS_CONFIG['private_key'],
            'https://www.googleapis.com/auth/analytics')
        http_auth = credentials.authorize(Http())
        analytics = build('analytics', 'v3', http=http_auth)

        # Copy defaults
        query_options = dict(self.DEFAULT_QUERY_OPTIONS)

        # External content have special urls
        for (key, filters) in self.KEY_FILTERS.items():
            print 'Fetching most read for key "{}"'.format(key)

            query_options['filters'] = filters
            query = analytics.data().ga().get(**query_options)
            results = query.execute()

            articles = defaultdict(int)
            for entry in results['rows']:
                # see `METRICS` for entry format
                page_path = entry[PAGE_URL]
                slug = self.slug_from_page_path(page_path)
                pageviews = int(entry[PAGEVIEWS])

                # Try to find the content from the url
                if '/topic/' in page_path:
                    matches = TopicPage.objects.filter(slug=slug)
                elif '/article/' in page_path:
                    date = self.date_from_page_path(page_path)
                    matches = Article.objects.filter(slug=slug,
                                                     issue__issue_date=date)
                else:
                    # Url does not match typically tracked content. Assume
                    # this is External Content
                    matches = ExternalContent.objects.filter(
                        redirect_url=page_path)

                # If there are duplicate slugs, assume the most recent
                cont = matches.order_by('-created_on').first()

                # If we found something, add it to our list
                if cont:
                    articles[cont] += pageviews
                else:
                    print 'ERROR: could not find %s' % page_path

            articles = sorted(articles.items(),
                              key=lambda x: x[1], reverse=True)[:5]
            for idx, article in enumerate(articles):
                print '\t{}. {}'.format(idx + 1,
                                        article[0].title.encode('utf-8'))

            if len(articles) == 5:
                most_read = MostReadArticles(key=key,
                                             article1=articles[0][0],
                                             article2=articles[1][0],
                                             article3=articles[2][0],
                                             article4=articles[3][0],
                                             article5=articles[4][0])
                most_read.save()
                cache_homepage.apply_async()
            else:
                print "\tCouldn't find five most read articles; skipping"
