import StringIO
import urllib

from django.http import HttpResponse

import PIL
import PIL.ImageDraw as imdraw

# import PIL.ImageEnhance as imenhance
# import PIL.ImageFont as imfont


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = PIL.ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def resize(im, targetWidth):
    targetHeight = int(targetWidth * float(im.size[1] / im.size[0]))
    return im.resize((targetWidth, targetHeight), PIL.Image.ANTIALIAS)


def watermark(im, credits, opacity=1):
    """Adds a watermark to an image."""
    # First resize mark to make it appropriate size
    logoURL = 'https://s3.amazonaws.com/static.thecrimson.com' + \
        '/images/feature/thc-logo-large.png'
    imfile = StringIO.StringIO(urllib.urlopen(logoURL).read())
    mark = PIL.Image.open(imfile)
    mark = mark.resize((100, 10), PIL.Image.ANTIALIAS)
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    # font = imfont.truetype(font='/static/fonts/ColabLig-webfont.ttf',
    # size=15, index=0, encoding='')
    layer = PIL.Image.new('RGBA', im.size, (0, 0, 0, 0))
    draw = imdraw.Draw(im)
    position = (im.size[0] - mark.size[0] - 10, 10)
    layer.paste(mark, position)
    # draw.text((x, y),"Sample Text",(r,g,b),font)
    draw.text((10, im.size[1] - 20), credits, (255, 255, 255))
    # composite the watermark with the layer
    watermarkedImage = PIL.Image.composite(layer, im, layer)
    response = HttpResponse(content_type='image/png')
    watermarkedImage.save(response, 'PNG')
    return response
