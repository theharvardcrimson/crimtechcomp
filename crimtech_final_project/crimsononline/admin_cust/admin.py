from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.contrib.redirects.admin import RedirectAdmin
from django.contrib.redirects.models import Redirect
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site

from social.apps.django_app.views import auth

from crimsononline.ads.admin import AdUnitAdmin
from crimsononline.ads.models import AdUnit, AdZone
from crimsononline.archive_photos.admin import ArchiveImageAdmin
from crimsononline.archive_photos.models import ArchiveImage
from crimsononline.content.admin import (
    ArticleAdmin, BreakingNewsAdmin, ContentGroupAdmin, ContributorAdmin,
    CorrectionAdmin, ExternalContentAdmin, FeaturePackageAdmin,
    FlashGraphicAdmin, GalleryAdmin, GenericFileAdmin, ImageAdmin, IndexAdmin,
    IssueAdmin, MapAdmin, PDFAdmin, ReviewAdmin, SectionAdmin, TableAdmin,
    TagAdmin, TopicPageAdmin, VideoAdmin, WidgetAdmin)
from crimsononline.content.models import (
    PDF, Article, BreakingNews, ContentGroup, Contributor, Correction,
    ExternalContent, FeaturePackage, FlashGraphic, Gallery, GenericFile, Image,
    Index, Issue, Map, Review, Section, Table, Tag, TopicPage, Video, Widget)
from crimsononline.content_module.admin import ContentModuleAdmin
from crimsononline.content_module.models import ContentModule
from crimsononline.newsletter.admin import (
    HarvardTodayNewsletterAdmin, NewsletterAdAdmin, NewsletterAdmin)
from crimsononline.newsletter.models import (
    HarvardTodayNewsletter, Newsletter, NewsletterAd)
from crimsononline.placeholders.admin import LayoutInstanceAdmin
from crimsononline.placeholders.models import LayoutInstance
from crimsononline.texteditors.widgets import UnsafeWYSIWYGEditor


class CrimsonAdminSite(AdminSite):
    site_header = 'The Crimson administration'
    site_title = 'The Crimson administration'

    def login(self, request, extra_context=None):
        if 'local' in request.GET:
            return super(CrimsonAdminSite, self).login(request, extra_context)
        return auth(request, backend='google-oauth2')

    def each_context(self, request):
        context = super(CrimsonAdminSite, self).each_context(request)
        context['is_development'] = self.is_development(request)
        return context

    def is_development(self, request):
        """Whether this request seems to be against a development host"""
        return request.get_host() in settings.DEVELOPMENT_HOSTS


site = CrimsonAdminSite()


class WYSIWYGFlatpageForm(FlatpageForm):
    class Meta(FlatpageForm.Meta):
        widgets = {
            'content': UnsafeWYSIWYGEditor()
        }


class WYSIWYGFlatPageAdmin(FlatPageAdmin):
    form = WYSIWYGFlatpageForm


# django.contrib.auth
site.register(Group, GroupAdmin)
site.register(User, UserAdmin)

# django.contrib.flatpages
site.register(FlatPage, WYSIWYGFlatPageAdmin)

# django.contrib.redirects
site.register(Redirect, RedirectAdmin)

# django.contrib.sites
site.register(Site, SiteAdmin)

# crimsononline.ads
site.register(AdUnit, AdUnitAdmin)
site.register(AdZone)

# crimsononline.archive_photos
site.register(ArchiveImage, ArchiveImageAdmin)

# crimsononline.content
site.register(Article, ArticleAdmin)
site.register(BreakingNews, BreakingNewsAdmin)
site.register(ContentGroup, ContentGroupAdmin)
site.register(Contributor, ContributorAdmin)
site.register(Correction, CorrectionAdmin)
site.register(ExternalContent, ExternalContentAdmin)
site.register(FeaturePackage, FeaturePackageAdmin)
site.register(FlashGraphic, FlashGraphicAdmin)
site.register(Gallery, GalleryAdmin)
site.register(GenericFile, GenericFileAdmin)
site.register(Image, ImageAdmin)
site.register(Index, IndexAdmin)
site.register(Issue, IssueAdmin)
site.register(Map, MapAdmin)
site.register(PDF, PDFAdmin)
site.register(Review, ReviewAdmin)
site.register(Section, SectionAdmin)
site.register(Table, TableAdmin)
site.register(Tag, TagAdmin)
site.register(TopicPage, TopicPageAdmin)
site.register(Video, VideoAdmin)
site.register(Widget, WidgetAdmin)

# crimsononline.content_module
site.register(ContentModule, ContentModuleAdmin)

# crimsononline.newsletter
site.register(HarvardTodayNewsletter, HarvardTodayNewsletterAdmin)
site.register(NewsletterAd, NewsletterAdAdmin)
site.register(Newsletter, NewsletterAdmin)

# crimsononline.placeholders
site.register(LayoutInstance, LayoutInstanceAdmin)
