from email.utils import parseaddr

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

import mailchimp
from PIL import Image as PILImage

from .middleware import NewsletterSubscribeMiddleware


class SubscribeView(TemplateView):
    template_name = 'newsletter/subscribe.html'

    TAGLINES = {
        'alumni': (
            'Cambridge is calling.',
            "Sign up to get alerted when there's important Harvard news.",
        ),
        'sports': (
            '42 sports. One newsletter.',
            "Watching every game so you don't have to.",
        ),
        'default': (
            'Get breaking news.',
            'Sign up for alerts, sent straight to your inbox.'
        )
    }

    def get_context_data(self, **kwargs):
        form_type = kwargs.get('form_type') or 'default'
        tagline = self.TAGLINES.get(form_type)
        if not tagline:
            raise Http404
        return {
            'form_type': form_type,
            'tagline': tagline,
            'utm_src': self.request.GET.get('utm_src'),
        }


def subscribe_online(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            if not ('@' in parseaddr(email)[1]):
                raise KeyError

        except KeyError:
            return HttpResponse('failure: no email provided')

        groups = request.POST.getlist('groups', [])
        groupings = [{
            'id': 2201,
            'groups': groups
        }]
        school_affiliation = request.POST.get('SCHLAFFIL', '')
        university_affiliation = request.POST.get('UNIVAFFIL', '')
        class_year = request.POST.get('CLASS', '')
        zipcode = request.POST.get('ZIPCODE', '')

        data = {
            'groupings': groupings,
            'SCHLAFFIL': school_affiliation,
            'UNIVAFFIL': university_affiliation,
            'CLASS': class_year,
            'ZIPCODE': zipcode,
            'UTM_SRC': request.POST.get('UTM_SRC', '').lower(),
            'FORM_VRSN': request.POST.get('FORM_VRSN', '').lower()
        }

        m = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        m.lists.subscribe(
            id='160d75b318',
            email={'email': email},
            merge_vars=data,
            email_type='html',
            double_optin=False,
            update_existing=True,
            replace_interests=False
        )

        return HttpResponse('success')
    else:
        return render(
            request,
            'forms/interstitial_subscribe.html',
            {'source': 'interstitial',
             'tagline': SubscribeView.TAGLINES['default']})


def subscribe_track(request):
    """
    Disables subscribe form interstitial for one month from the current
    day; renders 1x1 GIF

    To prevent email newsletter subscribers from having to see the
    subscribe form popup, all email newsletters include an <img> to this
    view, which disables our interstitial subscribe form for one month.
    Fails silently on malformed cookie.
    """

    response = HttpResponse(content_type='image/gif')

    NewsletterSubscribeMiddleware.record_newsletter_interaction(
        request, response)

    im = PILImage.new('1', (1, 1), color=0)
    im.save(response, 'GIF', transparency=0)

    return response
