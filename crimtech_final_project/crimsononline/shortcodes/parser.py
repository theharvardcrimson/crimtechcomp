import logging
import re
import shlex

from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def import_parser(name):
    try:
        mod = __import__(name)
    except UnicodeEncodeError:
        raise ImportError

    components = name.split('.')
    try:
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    except:
        return None


TRANSLATIONS = {
    u'\u00a0': ' ',
    u'\u2018': '\'',
    u'\u2019': '\'',
    u'\u201c': '"',
    u'\u201d': '"',
    '\n': '',
    '&nbsp;': ' ',
    '&lsquo;': '\'',
    '&ldquo;': '"',
    '&rsquo;': '\'',
    '&rdquo;': '"',
}


def parse(html):
    if isinstance(html, str):
        html = html.decode('utf-8')
    ex = re.compile(r'{(.*?)}', re.DOTALL)
    groups = ex.findall(html)

    count = 0  # number of times shortcodes are used in a single article

    for item in groups:
        clean_item = item
        for key, rep in TRANSLATIONS.iteritems():
            clean_item = clean_item.replace(key, rep)
        clean_item = strip_tags(clean_item).encode('utf-8')

        try:
            values = shlex.split(clean_item)
        except ValueError:
            continue  # skip malformed blocks

        # fix spaces around "="
        i = 0
        while i < len(values):
            if i > 0 and i + 2 <= len(values) and values[i] == '=':
                values[i - 1:i + 2] = ['{}{}{}'.format(*values[i - 1:i + 2])]
            elif (values[i] and i + 2 <= len(values) and
                    values[i][-1] == '='):
                values[i:i + 2] = ['{}{}'.format(*values[i:i + 2])]
                i += 1
            elif (i > 0 and i + 1 <= len(values) and values[i] and
                    values[i][0] == '='):
                values[i - 1:i + 1] = ['{}{}'.format(*values[i - 1:i + 1])]
            else:
                i += 1

        if len(values) > 0:
            name = values[0]
            args = _parse_args(values[1:])

            module = None

            try:
                module = import_parser(
                    'crimsononline.shortcodes.parsers.' + name)
            except ImportError:
                pass

            if module:
                function = getattr(module, 'parse')
                count += 1
                try:
                    result = function(args, count)
                except TypeError:
                    # wrong func signature
                    result = function(args)
                # cache.set(clean_item, result, 3600)
                html = html.replace('{' + item + '}', result, 1)

    # import highcharts api only once
    html = html.replace(
        '{{ highcharts import }}',
        '<script src="%sscripts/Highcharts/highcharts.js"></script>'
        '<script src="%sscripts/Highcharts/modules/exporting.js"></script>' %
        (settings.STATIC_URL, settings.STATIC_URL), 1)
    html = html.replace('{{ highcharts import }}', '')

    # import google visualization api only once
    html = html.replace(
        '{{ d3 import }}',
        '<script src="%sscripts/d3/d3.min.js"></script>' %
        (settings.STATIC_URL,), 1)
    html = html.replace('{{ d3 import }}', '')

    return html


def _parse_args(values):
    kwargs = {}

    for group in values:
        try:
            key, value = group.split('=', 1)
            kwargs[key] = value
        except ValueError:
            pass  # this is not a KV pair

    return kwargs
