# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import gc
import re

from django.conf import settings
from django.db import migrations, models
from django.db.models import Q

# Regex for finding shortcodes with a size parameter.
# Splits regex into chunks of first, size=??, last
# We'll later put the shortcode back together
reg_patt = r"""{(([^}]+?)\s)?size\s?=\s?('(\w+)'|"(\w+)"|(\w+))\s?([^}]*)}"""

def queryset_iterator(queryset, chunksize=50):
    """Queryset iterator from https://djangosnippets.org/snippets/1949/

    Iterates more memory-efficiently. Orders by primary key and takes
    slices of results from the query set.
    """
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()

def get_parts(match):
    """Extracts the sections of the found shortcode from regex.

    Inspects the match groups that come in from regex."""
    size = match.group(4)
    if not size:
        size = match.group(5)
    if not size:
        size = match.group(6)
    first = match.group(2)
    last = match.group(7)
    # Build tuple of results including the spaces that we need
    # If first/last exist, make sure they have space before/after
    first = unicode(first) + (' ' if first else '')
    last = (' ' if last else '') + unicode(last)
    return (first, size, last)

def rename_shortcode_sizes(apps, schema_editor):
    """Forward migration to rename the shortcode sizes in database."""
    def replace_sizes(match):
        """Performs the name replacement."""
        first, size, last = get_parts(match)
        if size.lower() == 'hefty':
            size = 'xlarge'
        elif size.lower() == 'xlarge':
            size = 'fullscreen'
        # Rebuild the shortcode "{{" is an escape for "{" in format str
        return u'{{{}size={}{}}}'.format(first, size, last)
    Article = apps.get_model('content', 'Article')
    # Long query to find articles containing "hefty" or "xlarge"
    contains_filter = Q(text__icontains='hefty') | Q(text__icontains='xlarge')
    query = Article.objects.only('text').all().filter(contains_filter)
    for art in queryset_iterator(query):
        # Use python regex find-replace to rename sizes.
        art.text = re.sub(reg_patt, replace_sizes, art.text)
        art.save()

def undo_rename_shortcode_sizes(apps, schema_editor):
    """Reverse of the forward migration. This is line-for-line

    The opposite of the above. See comments in forward migration
    for this one."""
    def replace_sizes(match):
        first, size, last = get_parts(match)
        if size.lower() == 'xlarge':
            size = 'hefty'
        elif size.lower() == 'fullscreen':
            size = 'xlarge'
        return u'{{{}size={}{}}}'.format(first, size, last)
    Article = apps.get_model('content', 'Article')
    contains_filter = Q(text__icontains='xlarge') | Q(text__icontains='fullscreen')
    query = Article.objects.only('text').all().filter(contains_filter)
    for art in queryset_iterator(query):
        art.text = re.sub(reg_patt, replace_sizes, art.text)
        art.save()

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20150327_1718'),
    ]

    operations = [
        migrations.RunPython(rename_shortcode_sizes,
                             undo_rename_shortcode_sizes),
    ]
