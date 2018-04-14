from django.conf import settings
from django.shortcuts import render_to_response


def offline(request):
    context = {
        'title': 'Administration offline',
        'contact': settings.READ_ONLY_CONTACT
    }
    return render_to_response('admin_cust/read_only.html', context)
