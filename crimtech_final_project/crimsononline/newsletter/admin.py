import logging

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ungettext

import mailchimp

from .models import (
    HarvardTodayEvent, HarvardTodayNewsletter, HarvardTodaySponsoredEvent,
    Newsletter, NewsletterAdFill)

from crimsononline.placeholders.models import Layout, LayoutInstance
from crimsononline.texteditors.widgets import WYSIWYGEditor

logger = logging.getLogger(__name__)


class NewsletterAdmin(admin.ModelAdmin):
    fields = ('newsletter_type', 'admin_link', 'send_date', 'ab_split',
              'subject', 'text')
    readonly_fields = ('admin_link',)
    list_display = ('newsletter_type', 'send_date')
    list_display_links = ('newsletter_type', 'send_date')
    list_per_page = 30
    actions = ('publish_mailchimp',)

    def admin_link(self, instance):
        obj = instance.layout_instance
        f = (obj._meta.app_label, obj._meta.model_name)
        url = reverse('admin:%s_%s_change' % f, args=[obj.id])
        return mark_safe(
            u'<a target="_blank" href="{u}">Edit</a>'.format(u=url))
    admin_link.allow_tags = True
    admin_link.short_description = 'LayoutInstance Admin Link'

    def get_urls(self):
        urls = super(NewsletterAdmin, self).get_urls()
        urls = [
            url(r'^(?P<obj_id>\d+)/preview/$',
                self.admin_site.admin_view(self.preview_newsletter)),
        ] + urls
        return urls

    def preview_newsletter(self, request, obj_id):
        n = Newsletter.objects.get(pk=obj_id)
        return HttpResponse(n.get_output())

    def queryset(self, request):
        qs = super(NewsletterAdmin, self).queryset(request)
        return qs.exclude(newsletter_type=2)

    def publish_mailchimp(self, request, queryset):
        m = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
        list_id = m.lists.list(
            {'list_name': 'Email Newsletter'})['data'][0]['id']

        for n in queryset:
            if not n.subject:
                self.message_user(
                    request,
                    '"%s" is missing subject. Publish canceled.' % n,
                    'ERROR')
                return

        for n in queryset:
            html = n.get_output()
            # MailChimp requires subject_a and subject_b to be different.
            # Generate a "different" subject_b that won't cause any mishaps.
            ab_subject_b = n.subject + '...'
            ab_options = {'split_test': 'subject',
                          'pick_winner': 'opens',
                          'split_size': 50,
                          'subject_a': n.subject,
                          'subject_b': ab_subject_b}
            if n.ab_split:
                nl_type = 'absplit'
                nl_type_opts = {'absplit': ab_options}
            else:
                nl_type = 'regular'
                nl_type_opts = None
            m.campaigns.create(nl_type,
                               {'list_id': list_id,
                                'subject': n.subject,
                                'from_email': 'no-reply@thecrimson.com',
                                'from_name': 'The Harvard Crimson',
                                'to_name': '*|FNAME|*',
                                'title': unicode(n)},
                               {'html': html},
                               type_opts=nl_type_opts)
        count = len(queryset)
        self.message_user(request, ungettext(
            'Successfully published %d newsletter to Mailchimp.',
            'Successfully published %d newsletters to Mailchimp.',
            count) % count)

    publish_mailchimp.short_description = 'Publish to Mailchimp'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.layout_instance = LayoutInstance.objects.create(
                name=unicode(obj),
                parent=Layout.objects.get(name=obj.get_default_layout()))

        super(NewsletterAdmin, self).save_model(request, obj, form, change)


class HarvardTodayEventInline(admin.StackedInline):
    model = HarvardTodayEvent
    extra = 0
    fields = ('time', 'description')

    formfield_overrides = {
        models.TextField: {
            'widget': WYSIWYGEditor()
        },
    }


class HarvardTodaySponsoredEventInline(admin.StackedInline):
    model = HarvardTodaySponsoredEvent
    extra = 1
    fields = ('time', 'description')

    formfield_overrides = {
        models.TextField: {
            'widget': WYSIWYGEditor()
        },
    }


class HarvardTodayNewsletterAdmin(NewsletterAdmin):
    fields = ('admin_link', 'send_date', 'ab_split', 'subject',
              'text', 'photo_description', 'weather_description',
              'lunch_description', 'dinner_description', 'article_list',
              'others_list')
    inlines = [HarvardTodayEventInline, HarvardTodaySponsoredEventInline]

    formfield_overrides = {
        models.TextField: {
            'widget': WYSIWYGEditor()
        },
    }

    def get_urls(self):
        urls = super(HarvardTodayNewsletterAdmin, self).get_urls()
        urls = [
            url(r'^(?P<obj_id>\d+)/preview/$',
                self.admin_site.admin_view(self.preview_newsletter)),
        ] + urls
        return urls

    def queryset(self, request):
        # get rid of override from NewsletterAdmin
        return super(NewsletterAdmin, self).queryset(request)

    def preview_newsletter(self, request, obj_id):
        n = HarvardTodayNewsletter.objects.get(pk=obj_id)
        return HttpResponse(n.get_output())


class NewsletterAdFillInline(admin.StackedInline):
    model = NewsletterAdFill
    extra = 0


class NewsletterAdAdmin(admin.ModelAdmin):
    inlines = [NewsletterAdFillInline]
