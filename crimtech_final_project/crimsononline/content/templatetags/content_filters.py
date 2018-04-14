import json
import logging
import string
from datetime import date, datetime
from re import DOTALL, compile

from django import template
from django.conf import settings
from django.template import defaultfilters as filter
from django.utils.safestring import mark_safe

from easy_thumbnails.exceptions import InvalidImageFormatError
from PIL import Image as PILImage

from crimsononline.common.templatetags.common import human_list, linkify
from crimsononline.common.utils.html import para_list
from crimsononline.common.utils.urlnames import urlname
from crimsononline.content.models import (
    Article, ArticleContentRelation, Content, Image, Marker, Tag)

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter
def render(content, method):
    if not content:
        return ''
    return mark_safe(content._render(method))


@register.filter
def datify(cont):
    """A more natural way to express dates on content.

    Uses the modified date if its recent, otherwise, uses issue_date
    """
    try:
        issue = cont.issue.issue_date
        if(date.today() <= issue):
            secs_ago = (datetime.today() - cont.modified_on).seconds
            if secs_ago < 3600:
                value = secs_ago / 60
                unit = 'minute'
            else:
                value = secs_ago / 3600
                unit = 'hour'
        else:
            daysold = (date.today() - issue).days
            if daysold == 1:
                return 'Yesterday'
            elif daysold <= 10:
                value = daysold
                unit = 'day'
            else:
                return issue.strftime('%B %d, %Y')
        plural = 's' if value != 1 else ''
        return '%d %s%s ago' % (value, unit, plural)
    except:
        return ''


@register.filter
def to_img_layout(img, dimensions):
    tag = ''
    if isinstance(img, Image):
        width, height = img.pic.width, img.pic.height
        w_constr, h_constr = tuple(dimensions.split(',')[:2])
        if width > height:
            type = 'wide'
            w_constr = str(int(int(w_constr) * 0.65) if w_constr else width)
        else:
            type = 'tall'
            w_constr = str(int(int(w_constr) * 0.40) if w_constr else width)
        img_tag = to_img_tag(img, w_constr + ',' + h_constr)
        tag = """<div class="%s_photo">%s
            <p class="byline">%s</p>
            <p class="caption">%s</p>
            </div>""" % (type, img_tag, linkify(img.contributor),
                         filter.force_escape(img.caption))
    return mark_safe(tag)


@register.filter
def img_caption(img):
    return mark_safe(img.child.caption)


@register.filter
def img_gallery_margin(img):
    """Gets the margin needed for an image in a gallery (height 450px)"""
    if float(img.pic.height) / img.pic.width >= 450.0 / 619.0:
        if img.pic.height >= 450:
            return 0
        return int(450 - img.pic.height) / 2
    else:
        ren_height = float(img.pic.height) / img.pic.width * 619
        return int(450 - ren_height) / 2


@register.filter
def to_img_tag(img, size_spec):
    """Turns an Image or ImageGallery into an img tag (html).

    @size_spec => the size spec of the display image. 3 possible formats:
        string name of the size_spec defined in the Image model
            (without the SIZE_ prefix),
        string formatted "WIDTH,HEIGHT,CROP_W,CROP_H" or "WIDTH,HEIGHT", or
        tuple given as (WIDTH, HEIGHT, CROP_W, CROP_H) or (WIDTH, HEIGHT)

    empty or omitted constraints are not binding
    any empty or zero crop parameter = no cropping
    """
    if img is None:
        return ''
    if img.__class__ is Content:
        img = img.child
    disp_url = img_url(img, size_spec)
    k = filter.force_escape(getattr(img, 'img_title', ''))
    tag = '<img src="%s" title="%s" alt="%s" />' % (disp_url, k, k)
    return mark_safe(tag)


@register.filter
def full_img_tag(img):
    """
    Gives out an img tag that uses the full-res version of an Image.
    """
    try:
        if img.__class__ is Content:
            img = img.child
        disp_url = img.absolute_url()
        title = filter.force_escape(getattr(img, 'img_title', ''))
        tag = '<img src="%s" title="%s" alt="%s" />' % (disp_url, title, title)
        return mark_safe(tag)
    except:
        return ''


@register.filter
def img_url(img, size_spec):
    if img.__class__ is Content:
        img = img.child
    # oh lawd almighty
    if not img or not hasattr(img, 'display_url'):
        return ''
    if isinstance(size_spec, tuple) or isinstance(size_spec, list):
        size_spec = [s or 0 for s in size_spec]
    else:
        # size_spec must be a string if it's not a tuple or list
        size_spec = str(size_spec)
        # This is a bit of a kludge -- it's to test whether the s_s has the
        # Upscale attribute specified
        if size_spec.count(',') == 4:
            size_spec = size_spec[:size_spec.rfind(',')]
        s = getattr(Image, 'SIZE_' + size_spec, None)
        if not s:
            size_spec = size_spec.replace('(', '').replace(')', '')
            size_spec = [sz or 0 for sz in size_spec.split(',')]
            for i in range(len(size_spec)):
                try:
                    size_spec[i] = int(size_spec[i])
                except ValueError:
                    try:
                        size_spec[i] = float(size_spec[i])
                    except ValueError:
                        pass
        else:
            size_spec = s
    if len(size_spec) < 3:
        size_spec = list(size_spec[:2]) + [0, 0]
    size_spec = tuple(size_spec)

    try:
        return mark_safe(img.display_url(size_spec))
    except InvalidImageFormatError:  # this is not an image
        return ''


@register.filter
def height_for_width(img, width):
    width = int(width)
    try:
        ratio = float(img.pic.height) / float(img.pic.width)
    except:
        try:
            ratio = float(img.main_rel_content.pic.height) / \
                float(img.main_rel_content.pic.width)
        except:
            return 0

    return int(ratio * width)


@register.filter
def multiply(first, second):
    return int(first * float(second))


@register.filter
def fm_img_tag(img, size_spec):
    if img is None:
        return mark_safe(
            '<img src="%s" title="%s" alt="%s" width="%s" height="%s" />' %
            (settings.STATIC_URL + 'images/fm-default.jpg',
             'Default Story Image', 'Default Story Image',
             size_spec.split(',')[0], size_spec.split(',')[1]))
    else:
        return to_img_tag(img, size_spec)


@register.filter
def large_fm_img_tag(img, size_spec):
    if img is None:
        return mark_safe(
            '<img src="%s" title="%s" alt="%s" width="%s" height="%s" />' %
            (settings.STATIC_URL + 'images/fm-default-large.jpg',
             'Default Story Image', 'Default Story Image',
             size_spec.split(',')[0], size_spec.split(',')[1]))
    else:
        return to_img_tag(img, size_spec)


@register.filter
def to_thumb_tag(img):
    THUMB_SIZE = 96
    return to_img_tag(img, (THUMB_SIZE, THUMB_SIZE))


@register.filter
def to_map_thumb(map, size):
    """ Gets the url of a static image for a map

    @width, @height => width and height of box

    TODO: cache this
    """
    if len(size.split(',')) == 2:
        dims = size.split(',')
        width = dims[0]
        height = dims[1]
    else:
        width = size
        height = size

    GMaps_key = settings.GOOGLE_API_KEY

    markerstr = ''
    markers = Marker.objects.filter(map__pk=map.pk)
    for marker in markers:
        markerstr = markerstr + str(marker.lat) + ',' + str(marker.lng) + '|'

    tag = '<img src="http://maps.google.com/staticmap?center=%s,%s&zoom=%s' \
          '&size=%sx%s&maptype=mobile&key=%s&sensor=false&markers=%s" />' % (
              map.center_lat, map.center_lng, map.zoom_level, width, height,
              GMaps_key, markerstr)
    return mark_safe(tag)


@register.filter
def pretty_sport_name(sport):
    """ For use with the sports ticker - return the pretty name of the sport"""
    tuples = Article.SPORTS_TYPE_CHOICES
    for t in tuples:
        if t[0] == sport:
            return t[1]
    return ''


@register.filter
def rel_no_articles(rel_content):
    """The non articles in a list of rel_content"""
    return [c for c in rel_content if not isinstance(c.child, Article)]


@register.filter
def rel_articles(rel_content):
    """Return the articles in a list of rel_content."""
    return [c.article for c in rel_content if isinstance(c.child, Article)]


@register.filter
def byline(obj, type, contributors_attr='contributors'):
    """Get the byline from an article, properly pluralized"""

    str = 'By '

    try:
        contributors = getattr(obj, contributors_attr)
        count = contributors.count()
        if count is 0:
            return filter.upper('No Writer Attributed')
        links = linkify(contributors.all())
        str += human_list(links)

        if type == 'short':
            return mark_safe(str)

        # byline_type = getattr(obj, 'byline_type', None)
        if hasattr(obj, 'byline_type'):
            byline_type = obj.get_byline_type_display()
        else:
            byline_type = None
        if byline_type is not None and byline_type != 'None':
            str += ', ' + byline_type.upper()
            str += filter.pluralize(count).upper()

        return mark_safe(str)
    except AttributeError:
        return ''


@register.filter
def byline_multimedia(obj, type):
    byline_str = byline(obj, type, 'multimedia_contributors')
    return mark_safe(byline_str[0].lower() + byline_str[1:])


@register.filter
def byline_sans_by(obj, type):
    """Get the byline from an article, properly pluralized,
       but without the 'By' before the name(s)"""

    str = ''

    try:
        count = obj.contributors.count()
        if count is 0:
            return filter.upper('No Writer Attributed')
        if 'sponsor' in type:
            if type == 'sponsor_url':
                return mark_safe(obj.contributors.all()[0].get_absolute_url())
            elif type == 'sponsor_name':
                name = ''
                if obj.contributors.all()[0].first_name != ' ':
                    name += obj.contributors.all()[0].first_name + ' '
                if obj.contributors.all()[0].middle_name != '':
                    name += obj.contributors.all()[0].middle_name + ' '
                if obj.contributors.all()[0].last_name != ' ':
                    name += obj.contributors.all()[0].last_name
                return mark_safe(name)
            elif type == 'sponsor_tcbs':
                str += human_list(linkify(obj.contributors.all()[0]))
                return mark_safe(str)
            elif type == 'sponsor_byline_second':
                try:
                    str += human_list(linkify(obj.contributors.all()[1]))
                except:
                    str += 'missing second contributor'
                return mark_safe(str)
            elif type == 'sponsor_byline':
                if count == 2:
                    str += human_list(linkify(obj.contributors.all()[1]))
                else:
                    str += human_list(linkify(obj.contributors.all()[0]))
                return mark_safe(str)
        links = linkify(obj.contributors.all())
        str += human_list(links)

        if type == 'short':
            return mark_safe(str)

        # byline_type = getattr(obj, 'byline_type', None)
        if hasattr(obj, 'byline_type'):
            byline_type = obj.get_byline_type_display()
        else:
            byline_type = None
        if byline_type is not None and byline_type != 'None':
            str += ', ' + byline_type.upper()
            str += filter.pluralize(count).upper()

        return mark_safe(str)
    except AttributeError:
        return ''


@register.filter
def fix_teaser(teaser):
    """Fixes the messed-up Flyby teasers that show up on writer pages."""
    teaser_paras = para_list(teaser)
    try:
        return teaser_paras[0]
    # I think this shouldn't happen, but better safe than sorry...
    except IndexError:
        return ''


@register.filter
def has_jump(flybyarticle):
    """Checks whether a Flyby article has content past the jump.  Returns
    a boolean value that tells the Flyby content list template whether to
    display the "continued" link."""
    if flybyarticle.teaser != '':
        fba_paras = para_list(flybyarticle.text)
        teaser_paras = para_list(flybyarticle.teaser)
        if len(fba_paras) > len(teaser_paras):
            return True
        else:
            return False
    else:
        return (flyby_teaser(flybyarticle) != '')


@register.filter
def flyby_teaser(flybyarticle):
    """Processes a flybyarticle, returning the portion before the jump
    assuming that the article uses the new jump tag method.  If it doesn't,
    it returns ""."""
    jumptagre = compile(r'(.*)<!--more-->', DOTALL)
    match = jumptagre.match(flybyarticle.text)
    # If we find the tag, return the captured stuff before it
    if match:
        return match.group(1)
    # If we don't find the tag, this article has no jump.  Return
    # nothing so that the template recognizes this and just spits out
    # the text.
    else:
        return ''


@register.filter
def jump_to_anchor(text):
    """Removes the <!--more--> tag from a Flyby article, replacing it with an
    <a name="jump"/> instead."""
    jumprepre = compile(r'<!--more-->')
    parsedtext = jumprepre.sub('<a name="jump"></a>', text)
    return parsedtext


@register.filter
def is_flyby_quote(flybyarticle):
    """Checks for a special Flyby Quote Tag among an article's tags.  If it has it,
    returns true."""
    quotetag = Tag.objects.get(text='Flyby Quote')
    if quotetag in flybyarticle.tags.all():
        return True
    return False


@register.filter
def render_rc_sub(rc, counter):
    """Renders inline images in Flyby articles."""
    rc = rc.exclude(content_type__model='article')
    # Add 1 since presumably the top rc is already accounted for
    index = counter / 2
    try:
        content = rc[index]
    except IndexError:
        return ''
    if index % 2 == 0:
        return mark_safe(content._render('flyby.inline_left'))
    else:
        return mark_safe(content._render('flyby.inline_right'))


@register.filter
def flyby_series_imgwidth(series, totalwidth):
    """Calculates the number of pixels left for the series top img once the tabs
    are accounted for."""
    count = len(series)
    # TODO MAGIC NUMBER
    return str(int(totalwidth) - 20 * (count - 1))


@register.filter
def flyby_series_imgoffset(series, totalwidth):
    """Calculates the offset for an image so that the center is always what's
    exposed behind the tabs."""
    count = len(series)
    # TODO MAGIC NUMBER
    return str((20 * (count - 1)) / 2)


@register.filter
def flyby_series_bgoffset(series, totalwidth):
    """Calculates the offset for the background image so that it matches when one
    mouses over the last thing in the series."""
    count = len(series)
    # TODO MAGIC NUMBER
    return str((20 * count) - ((20 * (count - 1)) / 2))


@register.filter
def self_or_first(object):
    """
    Returns the first object in a list or the object itself if not a list.
    """
    try:
        return object[0]
    except:
        return object


@register.filter
def get_image_obj(article):
    if article.__class__ == Image:
        return article
    elif article.main_rel_content:
        return article.main_rel_content
    else:
        arcs = ArticleContentRelation.objects \
                                     .filter(article=article) \
                                     .order_by('order')
        images = [x.related_content
                  for x in arcs
                  if x.related_content.content_type.model == 'image']
        images += [x.related_content.child.pic
                   for x in arcs
                   if x.related_content.content_type.model == 'flashgraphic']
        if len(images) > 0:
            return images[0]
        else:
            return None


@register.filter
def get_first_img(gallery):
    # gets the first image in a gallery
    if gallery.content_type.model != 'gallery':
        return None
    imgs = [x.content.image for x in gallery.gallery_set.all()
            if x.content.content_type == 'image']
    if len(imgs) > 0:
        return imgs[0]
    else:
        return None


@register.filter
def get_flyby_category(article):
    flyby_categories = ['Campus', 'Culture', 'City', 'Politics', 'Arts']
    for a in article.tags.all():
        if a.text.startswith('Flyby'):
            try:
                if a.text.split()[1] in flyby_categories:
                    return a.text.split()[1]
            except IndexError:
                continue
    # Fail silently
    return ''


@register.filter
def urlify(content):
    return urlname(content)


@register.filter
def shortentext(text, length):
    s = text[0:int(length)]
    if s == text:
        return text
    while s[-1] != ' ' and not s[-1] in set(string.punctuation):
        s = s[0:-1]
    return s.strip() + '...'


def gradient_processor(im, grad=False, color='white', max_opacity=100.,
                       min_opacity=0., direction='UP', **kwargs):

    if not grad:
        return im

    UP = 'UP'
    DOWN = 'DOWN'
    DIRS = [UP, DOWN]

    max_opacity = min(255., max_opacity) * 255. / 100.
    min_opacity = max(0., min_opacity) * 255. / 100.
    if direction.upper() not in DIRS:
        direction = UP

    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    gradient_mask = PILImage.new('L', (1, im.size[1]))
    height = gradient_mask.size[1]

    print '\n\nNEW IMAGE'
    print 'HEIGHT: {0}'.format(im.size[1])
    for y in range(height):
        grad_opacity = (max_opacity - min_opacity) / (height) * (y + 1)
        grad_opacity += min_opacity
        gradient_mask.putpixel((0, y), 255. - grad_opacity)

    if direction == DOWN:
        gradient_mask = gradient_mask.rotate(180)

    mask = gradient_mask.resize(im.size, PILImage.ANTIALIAS)
    background = PILImage.new('RGBA', im.size, color)
    return PILImage.composite(im, background, mask)


@register.filter
def ctype(obj):
    return obj.__class__.__name__


@register.filter
def parse_json(s):
    return json.loads(s)


@register.filter(name='zip')
def _zip(a, b):
    return list(zip(a, b))
