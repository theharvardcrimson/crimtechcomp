from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from crimsononline.content.models import Content, Tag


@cache_page(settings.CACHE_STANDARD)
def index(request):
    # Get tags
    tags = {
        'main_feat': get_object_or_404(Tag, text='March Madness Feature'),
        'feat_left': get_object_or_404(Tag, text='March Madness Feature Left'),
        'feat_right': get_object_or_404(Tag,
                                        text='March Madness Feature Right'),
        'other_left': get_object_or_404(Tag, text='March Madness Left'),
        'other_right': get_object_or_404(Tag, text='March Madness Right'),
    }

    # Build parallel dictionary with tags from dict above
    bracket_arts = {}
    for section, tag in tags.iteritems():
        if section.startswith('other'):
            bracket_arts[section] = [c.child
                                     for c in Content.objects.filter(tags=tag)
                                     .order_by('-created_on')[:2]]
        else:
            try:
                bracket_arts[section] = Content.objects.filter(tags=tag).\
                    order_by('-created_on')[0].child
            except:
                bracket_arts[section] = None

    # Get tags for sections
    section_tags = {
        'From the Bench': get_object_or_404(Tag, text='From the Bench'),
        'Around the Tournament': get_object_or_404(
            Tag, text='Around the Tournament'),
        'Breaking it Down': get_object_or_404(Tag, text='Breaking it Down'),
    }

    # Build some stuff
    other_sections = []
    for text, tag in section_tags.iteritems():
        sec_articles = [c.child for c in
                        Content.objects.filter(tags=tag)
                        .order_by('-created_on')[:5]]
        if len(sec_articles) > 0:
            other_sections.append({'title': text, 'articles': sec_articles})

    data = {
        'bracket_arts': bracket_arts,
        'other_sections': other_sections,
        's1name': 'On the Floor',
        's2name': 'By the Numbers',
        'hwins': 42,
        'hlosses': 11,
        'nav': 'sports',
        'ad_zone': 'SportsLanding',
    }

    return render(request, 'march_madness.html', data)
