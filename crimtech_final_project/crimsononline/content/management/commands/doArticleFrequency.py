import math
from datetime import datetime

from django.core.management.base import NoArgsCommand

from dateutil.relativedelta import relativedelta

from crimsononline.content.models import Article, Word
from crimsononline.content.recommended_articles import _article_freq


class Command(NoArgsCommand):
    help = """This command will update content.words to reflect the
              article frequency of articles created in the last
              year."""

    def handle_noargs(self, **options):
        """Generate word frequency of articles made in the last year."""

        # delete old words
        Word.objects.all().delete()

        now = datetime.now()
        # we're generating article frequency for articles created in last year
        after = datetime.now() - relativedelta(years=1)

        # create new article frequencies for every article in the last year
        article_set = Article.objects.filter(created_on__gt=after)
        article_freq = _article_freq(article_set)

        words = [w for w in article_freq.keys() if len(w) < 150]
        nwords = len(words)
        # break into log(N) batches
        batch = int(nwords / math.log(nwords, 2))

        # create new word objects in log(N)  bulk_creates (single query
        # per batch)
        for i in xrange(0, nwords, batch):
            Word.objects.bulk_create([
                Word(word=wrd, word_frequency=article_freq[wrd],
                     last_updated=now)
                for wrd in words[i: i + batch]])
