import gc
import math
import random
import re
import string
import sys
from collections import Counter
from HTMLParser import HTMLParser
from itertools import combinations

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from BeautifulSoup import BeautifulSoup
from dateutil.relativedelta import relativedelta

from crimsononline.content.models import (
    Article, ArticleKeywordRelation, Keyword, Word)

config = settings.REC_ARTICLES


def _combos(akrs, max_constraint=sys.maxint, min_constraint=0):
    """
    All combinations of a set of ArticleKeywordRelations, with best
    combos first.
    """
    combs = []
    for i in xrange(min_constraint, min(len(akrs), max_constraint) + 1):
        c = [list(set) for set in combinations(akrs, i)]
        combs.extend(c)
    combs.sort(key=lambda s: sum(akr.score for akr in s), reverse=True)
    return combs


def _tolkenize(article):
    """
    Returns article text, stripped of html tags, punctuation, and escape chars.
    """
    # escape unicode
    text = article.text.encode('ascii', 'ignore')

    # remove all html tags ('<p>') and make lower case
    text = ' '.join(BeautifulSoup(text).findAll(text=True)).lower()

    # remove shortcodes
    text = re.sub(r'{(.*?)}', ' ', text)

    # replace html entities with ' '
    text.replace(HTMLParser().unescape(text), ' ')

    # remove newline and carriage returns
    text = text.replace('\n', '  ').replace('\r', '  ')

    # strip punctuation from left and right of each word
    text = [word.strip(string.punctuation) for word in text.split()]

    # remove single-letter words and email addresses
    text = [word for word in text if not (len(word) < 2 or '@' in word)]

    return text


def _tfidf(word, narticles, tolkens, word_freq, article_freq):
    """
        Use term frequency-inverse document frequency to score the importance
        of a word in an article.
    """
    try:
        # Ratio of word frequency to total word count in text.
        tf = word_freq[word] / float(len(tolkens))
        # inverse document frequency of word: ratio of total size of
        # corpus to number of of articles containing word
        idf = 0
        if not article_freq[word]:
            idf = 1
        else:
            # use square of global word frequency to diminish score of
            # infrequent words
            idf = math.log(narticles / float(article_freq[word]))
        return round(tf * idf, 6)
    except ZeroDivisionError:
        return 0


def _create_article_freq(article_set):
    """ Number of articles that contain each word in a set of articles. """
    article_freq = Counter()
    set_query = article_set.iterator()
    for article in set_query:
        for word in Counter(_tolkenize(article)):
            article_freq[word] += 1
    return article_freq


def populate_global_article_freq():
    """
    Populates Word table with article frequencies from most recent articles.
    """
    Word.objects.all().delete()
    a = Article.objects.order_by('-created_on')[:config['CORPUS_SIZE']]
    af = _create_article_freq(a)

    count = 0
    limit = 100000  # only save 100000 most frequently used words
    for w in sorted(af, key=af.get, reverse=True)[:limit]:
        count += 1
        if count % 100 is 0:
            print '{0} / {1}'.format(count, limit)

        if len(w) < 150:
            word, created = Word.objects.get_or_create(
                word=w, defaults={'word_frequency': af[w]})
            if not created:
                word.word_frequency += af[w]
            word.save()


def _generate_keywords(article, article_freq=None, narticles=None):
    """ Generates keywords for article and saves. """
    tolkens = _tolkenize(article)
    if not tolkens:
        return

    if not article_freq:
        # query article frequencies
        article_freq = Counter()
        for tolken in tolkens:
            try:
                article_freq[tolken] = Word.objects.get(word=tolken) \
                                                   .word_frequency
            except ObjectDoesNotExist:
                # Counter() initializes undefined keys to 0
                continue

        # number of articles in corpus
        narticles = config['CORPUS_SIZE']

    # set up word frequencies with words from text
    wfreq = Counter(tolkens)

    # add words in title with a frequency = mean word frequency
    mean_freq = float(sum(wfreq[word] for word in wfreq)) / len(wfreq)
    wfreq.update({word: mean_freq for word in article.title.lower()})

    # generate keywords, create Keyword objects, and save to article
    keywords = {word: _tfidf(word, narticles, tolkens, wfreq, article_freq)
                for word in wfreq}

    # sort by increasing tf-idf score
    keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)

    for kw, sc in keywords[:config['NUM_KEYWORDS']]:
        if len(kw) < 150:
            new_kw, _ = Keyword.objects.get_or_create(word=kw)
            akr = ArticleKeywordRelation(article=article,
                                         keyword=new_kw,
                                         score=sc)
            akr.save()


def get_keywords(article):
    """ Generate keywords for a single article."""
    # delete old keywords
    article.keywords.all().delete()
    # create and save keywords
    _generate_keywords(article)
    return article


def get_keywords_all():
    """ Generate keywords for most recent 100k articles. """
    # Tell Django not to save all our changes to the database
    transaction.set_autocommit(False)

    queryset = Article.objects.filter(keywords=None).order_by('-created_on')
    chunksize = 20000
    narticles = queryset.count()
    outer = 0
    for i in xrange(0, narticles, chunksize):
        try:
            print 'Chunk ({0} - {1}) / {2}'.format(
                outer, outer + chunksize, narticles)
            chunk = queryset[i:i + chunksize]
            print 'Generating article frequency...'
            article_freq = _create_article_freq(chunk)
            print 'Finished generating article frequency...'
            inner = 0
            for article in chunk.iterator():
                if inner % 50 is 0:
                    print('\tGenerating keywords for article {0} / {1}'
                          .format(inner, chunksize))
                article.keywords.all().delete()
                _generate_keywords(article, article_freq, chunksize)
                inner += 1
            outer += chunksize
        except:
            transaction.rollback()
        finally:
            transaction.commit()
        chunk, article_freq = None, None
        gc.collect()

    # Turn autocommit back on
    transaction.set_autocommit(True)


def generate_by_keywords(art):
    """ Given an article, generate recommended articles using keywords. """
    # get article's kws and cache all other articles with assoc. with
    # each kw in memory query all AKRs through models for article
    akrs = ArticleKeywordRelation.objects.filter(article=art)
    if not akrs:
        return

    # sort combos by sum tf-idf score
    akr_cmbs = _combos(akrs,
                       min_constraint=config['MIN_KW_COMBO'],
                       max_constraint=config['MAX_KW_COMBO'])
    kw_cmbs = [[akr.keyword for akr in cmb] for cmb in akr_cmbs]
    rel_content = [a.pk for a in art.rel_content.all()]
    rec_articles = []
    for kw_set in kw_cmbs:
        # query all articles with each keyword in kw_set
        new_articles = Article.objects \
                              .exclude(pk__in=rel_content) \
                              .exclude(pk__in=[r.pk for r in rec_articles]) \
                              .exclude(pk=art.pk)

        for kw in kw_set:
            new_articles = new_articles.filter(keywords__pk=kw.pk)

        if not new_articles:
            continue

        # probabilistically accept older articles
        def datediff(a):
            return relativedelta(art.issue.issue_date, a.issue.issue_date).years

        def accept(a):
            if datediff(a) < config['RECENCY_CUTOFF']:
                return True
            else:
                return random.random() < config['ACCEPT_PROB']

        new_articles = filter(accept, new_articles)
        new_articles = sorted(new_articles, key=lambda a: a.issue.issue_date)

        rec_articles.extend(new_articles)

        # check if sufficient number of rec content has been found
        # if not, we continue by querying next kw_set
        if len(rec_articles) >= config['NUM_REC_ARTICLES']:
            break

    # only save the first NUM_REC_ARTICLES articles
    rec_articles = rec_articles[:config['NUM_REC_ARTICLES']]
    rec_articles = list(set(rec_articles))
    art.rec_articles.clear()
    art.rec_articles.add(*rec_articles)
    art.save()


def generate_rec_articles(article):
    """
    Wrapper that makes rec articles for article and regenerates
    rec_articles for each of article.rec_articles.
    """
    generate_by_keywords(article)
    for rec in article.rec_articles.all():
        generate_by_keywords(rec)
