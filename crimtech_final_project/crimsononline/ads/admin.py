from django.conf.urls import url
from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils.encoding import force_text

if False:
    from .networks import ad_network


class AdUnitAdmin(admin.ModelAdmin):
    list_display = ('code', 'network_id', 'display_on')
    list_filter = ('display_on',)
    search_fields = ('code', 'network_id')
    readonly_fields = ('code', 'network_id', 'size', 'display_on')
    actions = None

    def get_urls(self):
        urls = super(AdUnitAdmin, self).get_urls()
        new_urls = [
            url(r'^autoupdate/$',
                self.admin_site.admin_view(self.autoupdate_view),
                name='ads_adunit_autoupdate')
        ]
        return new_urls + urls

    def autoupdate_view(self, request):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        if request.method == 'POST':
            self.message_user(request, 'Auto-updating temporarily broken.',
                              messages.ERROR)
            if False:
                ad_network.update_ad_units()
                msg = ('Ad units updated from network successfully.')
                self.message_user(request, msg, messages.SUCCESS)
            return redirect('admin:ads_adunit_changelist')
        else:
            plural_name = force_text(self.model._meta.verbose_name_plural)
            context = {
                'title': 'Auto-update %s' % plural_name,
                'opts': self.model._meta
            }
            return render(request, 'admin/ads/adunit/autoupdate.html', context)

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
