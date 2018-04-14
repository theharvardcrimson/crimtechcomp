import copy
import csv
import hashlib
import json
import logging
import os
import re
import urllib
from datetime import date, datetime, timedelta
from itertools import combinations

from django import forms
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.core import exceptions
from django.core.cache import cache
from django.core.files import File
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.forms import ModelForm
from django.forms.utils import ErrorList
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import string_concat

from PIL import Image as pilImage
from solo.admin import SingletonModelAdmin

from crimsononline.common.caching import expire_page
from crimsononline.common.forms import (
    ContentGroupChoicesField, ContributorChoicesField,
    TopicPageSingleChoiceField)
from crimsononline.content.forms import (
    IssuePickerField, MapBuilderField, RelatedContentField, TagSelectWidget)
from crimsononline.content.generators import cache_homepage, purge_facebook
from crimsononline.content.models import (
    PDF, Article, ArticleContentRelation, Content, ContentGroup, ContentType,
    Contributor, Correction, ExternalContent, FeaturePackage,
    FeaturePackageSection, FlashGraphic, Gallery, GalleryMembership, Image,
    Index, Issue, Map, Marker, PackageSectionContentRelation, Review, Score,
    Section, Table, Tag, TopicPage, Video, Widget, youtube_get_save_path)
from crimsononline.placeholders.models import Layout, LayoutInstance
from crimsononline.texteditors.widgets import WYSIWYGEditor

logger = logging.getLogger(__name__)


class LimitedIssueListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Issue'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'limitedissue'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        issues = Issue.objects.all()[:50]
        return [(issue.id, issue.__unicode__, ) for issue in issues]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            issue = Issue.objects.get(id=self.value())
            return queryset.filter(issue=issue)


class ContentGroupModelForm(ModelForm):
    image = forms.ImageField(required=False,
                             widget=admin.widgets.AdminFileWidget)

    class Meta:
        model = ContentGroup
        fields = '__all__'


class ContentGroupAdmin(admin.ModelAdmin):
    form = ContentGroupModelForm


class ContentModelForm(ModelForm):
    """
    Parent class for Content model forms.

    Doesn't actually work by itself.
    """

    tags = forms.ModelMultipleChoiceField(
        Tag.objects.all(), required=True,
        widget=TagSelectWidget('Tags', False, tag_qs=Tag.objects.all())
    )

    contributors = ContributorChoicesField()

    issue = IssuePickerField(label='Issue Date', required=True)

    section = forms.ModelChoiceField(
        queryset=Section.objects.all(), required=True)
    priority = forms.ChoiceField(
        choices=Content.PRIORITY_CHOICES,
        required=False, initial=4, help_text='Higher priority articles are '
        'displayed first.'
    )
    group = ContentGroupChoicesField(required=False)
    delete_group = forms.BooleanField(
        initial=False, required=False, label='Clear Group')
    pub_status = forms.ChoiceField(
        Content.PUB_CHOICES, required=True,
        label='Published Status', help_text='Only execs can publish content.'
    )
    show_ads = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = Content
        fields = '__all__'

    def clean(self):
        cd = self.cleaned_data
        # make sure issue + slug are unique
        # no slug or no issues means there can't be a clash
        if 'slug' not in cd or 'issue' not in cd:
            return cd
        try:
            obj = Content.objects.admin_objects().get(
                slug=cd['slug'], issue=cd['issue']
            )
        except Content.DoesNotExist:
            # no content = no clash
            return cd

        if 'delete_group' in cd and cd['delete_group']:
            cd['group'] = None

        # it's an update, so, no clash
        if self.instance.pk and obj.pk == self.instance.pk:
            return cd
        msg = 'There is already content ' \
            'for this issue date with this issue and slug.  %%s' \
            '<a href="%s">See the other item.</a>' \
            % obj.get_admin_change_url()
        self._errors['slug'] = ErrorList([mark_safe(msg % '')])
        raise forms.ValidationError(mark_safe(
            msg % 'You should probably change the slug.'))


class ContentAdmin(admin.ModelAdmin):
    """
    Parent class for Content ModelAdmin classes.

    Doesn't actually work by itself.
    """

    # no ordering - faster retrieval
    exclude = []
    ordering = []
    actions = ['make_published', 'make_draft']

    def get_readonly_fields(self, request, obj=None):
        # XXX This isn't secure. Decide whether we care, because verifying this
        # properly is a huge pain, and Django's admin doesn't purport to be
        # secure anyway.
        additional_fields = []
        if not request.user.has_perm('content.can_hide_ads'):
            additional_fields += ['show_ads']
        if obj and obj.pub_status == 1:
            additional_fields += ['slug']
        return self.readonly_fields + tuple(additional_fields)

    def get_form(self, request, obj=None):
        f = super(ContentAdmin, self).get_form(request, obj)

        issue = f.base_fields['issue'].widget
        if obj is not None and int(obj.pub_status) is 1:
            issue.editable = False
        else:
            issue.editable = True
        if request.user.is_superuser:
            f.base_fields['tags'].required = False

        if request.user.has_perm('content.delete_content'):
            f.base_fields['pub_status'].widget.choices = Content.PUB_CHOICES
        elif request.user.has_perm('content.content.can_publish'):
            f.base_fields['pub_status'].widget.choices = \
                ((0, 'Draft'), (1, 'Published'),)
        else:
            f.base_fields['pub_status'].widget.choices = ((0, 'Draft'),)
        return f

    def save_model(self, request, obj, form, change):
        # don't let anyone change issue / slug on published content.
        new_status = int(obj.pub_status)
        if change:
            old_obj = self.model.objects.all_objects().get(pk=obj.pk)
            old_status = int(obj.original_pub_status)
        else:
            old_status = None

        if change and obj and new_status == 1:
            if ((obj.issue != old_obj.issue or obj.slug != old_obj.slug) and
                    old_status == 1):
                messages.add_message(
                    request, messages.INFO,
                    'You can\'t change '
                    'the issue or slug on published content.  Changes to '
                    'those fields have been undone.')
                obj.issue, obj.slug = old_obj.issue, old_obj.slug
            # don't let nonpermissioned users publish articles
            if old_status != 1 and not \
                    request.user.has_perm('content.content.can_publish'):
                raise exceptions.SuspiciousOperation()

            if old_status != 1:
                obj.created_on = datetime.now()
                # Change created_on to time published

        # don't let unpermissioned users delete content
        if not request.user.has_perm('content.content.can_delete') and \
                form.cleaned_data['pub_status'] is -1:
            raise exceptions.SuspiciousOperation()

        super(ContentAdmin, self).save_model(request, obj, form, change)

        # update caching if not draft or was published
        if new_status != 0 or old_status == 1:
            # clears cache for flyby box if necessary
            if obj.section.name == 'Flyby':
                cache.delete('flyby_preview')
            cache_homepage.apply_async()

    #  Prevents deletion of published content by users without the
    #  necessary permissions
    def delete_view(self, request, object_id, extra_context=None):
        obj = self.get_queryset(request).get(pk=object_id)

        # If it's published, require stricter permissions
        if (not request.user
            .has_perm('content.content.can_delete_published') and
                int(obj.pub_status) == 1):
            messages.add_message(
                request, messages.INFO,
                'You do not have permission to delete published articles.')
            change_url = reverse(
                'admin:content_%s_change' % self.model.ct().name,
                args=(object_id,))
            return redirect(change_url)

        # They have good permissions, or it's a draft, so let
        # ModelAdmin's delete_view handle the other permissions checks
        return super(ContentAdmin, self).delete_view(
            request, object_id, extra_context)

    # Prevent bulk-deletion of content by users without necessary permissions
    def get_actions(self, request):
        actions = super(ContentAdmin, self).get_actions(request)
        if not request.user.has_perm('content.content.can_delete_published'):
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        if request.user.has_perm('content.delete_content'):
            qs = self.model._default_manager.all_objects()
        elif request.user.has_perm('content.content.can_publish'):
            qs = self.model._default_manager.admin_objects()
        else:
            qs = self.model._default_manager.draft_objects()
        return qs

    # actions
    def make_published(self, request, queryset):
        if not request.user.has_perm('content.content.can_publish'):
            raise exceptions.PermissionDenied
        rows_updated = queryset.update(pub_status=1)
        if rows_updated == 1:
            message_bit = '1 object was'
        else:
            message_bit = '%s objects were' % rows_updated
        self.message_user(
            request, '%s successfully marked as published.' % message_bit)
    make_published.short_description = 'Publish content'

    def make_draft(self, request, queryset):
        if not request.user.has_perm('content.content.can_unpublish'):
            raise exceptions.PermissionDenied
        rows_updated = queryset.update(pub_status=0)
        if rows_updated == 1:
            message_bit = '1 object was'
        else:
            message_bit = '%s objects were' % rows_updated
        self.message_user(
            request, '%s successfully marked as draft.' % message_bit)
    make_draft.short_description = 'Mark content as Draft'


class TagForm(forms.ModelForm):
    ALLOWED_REGEXP = re.compile(r'[A-Za-z\s\'0-9]+$')

    class Meta:
        model = Tag
        fields = '__all__'

    def clean_text(self):
        text = self.cleaned_data['text']
        if not TagForm.ALLOWED_REGEXP.match(text):
            raise forms.ValidationError(
                'Tags can only contain letters and spaces')
        return text


class TagAdmin(admin.ModelAdmin):
    form = TagForm
    search_fields = ['text']
    ordering = ['text']


class ContributorForm(forms.ModelForm):
    bio_text = forms.CharField(
        widget=forms.Textarea, help_text='max 500 characters',
        required=False)
    image = forms.fields.ImageField(
        widget=admin.widgets.AdminFileWidget,
        required=False, label='Profile Picture')

    class Meta:
        model = Contributor
        fields = '__all__'

    def get_form(self, request, obj=None):
        # make a copy for this request only
        self.fieldsets = copy.deepcopy(self.raw_fieldsets)
        if not request.user.has_perm('content.make_unsearchable_content'):
            for name, field_options in self.fieldsets:
                cleaned_fields = tuple(
                    f for f in field_options['fields'] if f != 'searchable')
                field_options['fields'] = cleaned_fields
        return super(ArticleAdmin, self).get_form(request, obj)


def merge_contributors(modeladmin, request, queryset):
    contribs = list(queryset)
    # get the biggest profile:
    main_contrib = max(
        contribs, key=lambda c: len(Content.objects.filter(contributors=c)))
    contribs.remove(main_contrib)
    for c in contribs:
        content_list = list(Content.objects.filter(contributors=c))
        for content in content_list:
            content.contributors.remove(c)
            content.contributors.add(main_contrib)
        c.delete()


merge_contributors.short_description = 'Merge selected contributor profiles'


class ContributorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'middle_name')
    list_display = ('last_name', 'first_name', 'middle_name',
                    'created_on', 'is_active')
    list_display_links = ('last_name', 'first_name')
    list_filter = ('is_active',)
    readonly_fields = ('content_count',)
    actions = [merge_contributors]
    form = ContributorForm

    def content_count(self, obj):
        return len(Content.objects.filter(contributors=obj))

    def get_actions(self, request):
        actions = super(ContributorAdmin, self).get_actions(request)
        if not request.user.has_perm('content.contributor.can_merge'):
            del actions['merge_contributors']
        return actions


class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue_date',)
    search_fields = ('issue_date',)
    fields = ('issue_date', 'web_publish_date', 'special_issue_name',
              'fm_name', 'arts_name', 'comments',)

    def get_urls(self):
        urls = [
            url(r'^special_issue_list/$',
                self.admin_site.admin_view(self.get_special_issues)),
        ] + super(IssueAdmin, self).get_urls()
        return urls

    def get_special_issues(self, request):
        """
        Returns an html fragment with special issues as <options>
        """
        if request.method != 'GET':
            raise Http404
        year = request.GET.get('year', '')
        if not year.isdigit():
            raise Http404
        year = int(year)
        issues = Issue.objects.special.filter(issue_date__year=year)
        return render_to_response(
            'ajax/special_issues_fragment.html',
            {'issues': issues, 'blank': '----'})


class ImageAdminForm(ContentModelForm):
    class Meta:
        model = Image
        fields = '__all__'

    # the different sizes to crop. these should all be square sizes
    CROP_SIZES = (Image.SIZE_THUMB, Image.SIZE_TINY, Image.SIZE_SMALL)

    title = forms.fields.CharField(
        label='Kicker',
        widget=forms.TextInput(attrs={'size': '100'}))
    description = forms.fields.CharField(
        label='Caption', required=False,
        widget=forms.Textarea(attrs={'rows': '5', 'cols': '40'})
    )

    def clean(self):
        # limit max size of pic to 10MB
        try:
            if self.cleaned_data['pic']._size > 10 * 1024 * 1024:
                self._errors['pic'] = ErrorList([
                    mark_safe('This image is too large to upload for web.'
                              'Please shrink it first.')])
        except:
            pass  # either the image is missing or already uploaded

        return super(ImageAdminForm, self).clean()


class ImageAdmin(ContentAdmin):
    list_display = ('title', 'admin_thumb', 'pk', 'section', 'issue',
                    'pub_status')
    list_display_links = ('admin_thumb', 'title',)
    list_per_page = 30
    list_filter = ('section',)
    search_fields = ('title', 'description',)
    readonly_fields = ('admin_thumb', 'watermark_link',)

    fieldsets = (
        ('Image Setup', {
            'fields': ('pic', 'admin_thumb', 'description', 'title',
                       'watermark_link'),
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        ('Publication', {
            'fields': ('issue', 'section',),
        }),
        ('Web', {
            'fields': ('pub_status', 'priority', 'slug', 'tags', 'show_ads',),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        })
    )

    form = ImageAdminForm

    def get_queryset(self, request):
        return super(ImageAdmin, self).get_queryset(request).filter(
            is_archiveimage=False)

    def watermark_link(self, obj):
        return '<a target="_blank" href="/watermark/%s">watermark/%s</a>' \
            % (obj.pk, obj.pk)
    watermark_link.allow_tags = True
    watermark_link.short_description = 'Watermark Link'


class PDFAdminForm(ContentModelForm):
    class Meta:
        model = PDF
        fields = '__all__'

    contributors = ContributorChoicesField()

    def clean(self):
        # limit max size of PDF to 40MB
        try:
            if self.cleaned_data['document']._size > 40 * 1024 * 1024:
                self._errors['document'] = ErrorList([mark_safe(
                    'This file is too large to upload for web. '
                    'Please reduce its size.')])
        except:
            pass

        return super(PDFAdminForm, self).clean()


class PDFAdmin(ContentAdmin):
    form = PDFAdminForm

    list_display = ('title', 'pk', 'section', 'issue',
                    'pub_status')
    list_display_links = ('title',)
    list_per_page = 10
    list_filter = ('section',)

    fieldsets = (
        ('PDF', {
            'fields': ('title', 'description', 'document', 'thumbnail',),
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        (' ', {
            'fields': ('issue', 'section',),
        }),
        ('Web', {
            'fields': ('pub_status', 'priority', 'slug', 'tags',),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        })
    )

    def get_queryset(self, request):
        return super(PDFAdmin, self).get_queryset(request)


class GalleryForm(ContentModelForm):
    def __init__(self, *args, **kwargs):
        r = kwargs.get('instance', None)
        if r is not None:
            if 'initial' not in kwargs:
                kwargs['initial'] = {}
            kwargs['initial'].update({'contents_inline': r.admin_content_pks})
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields['pub_status'].help_text = """Warning: publishing this
            gallery will publish all content inside the gallery."""

    contents_inline = RelatedContentField(
        label='Contents', required=True,
        rel_types=[Image])
    layout = forms.ModelChoiceField(
        queryset=Layout.objects.filter(gallery_template=True),
        required=False, empty_label='Default')

    class Meta:
        model = Gallery
        fields = '__all__'


class GalleryAdmin(ContentAdmin):
    fieldsets = (
        ('Gallery Setup', {
            'fields': ('title', 'description'),
        }),
        ('Images', {
            'fields': ('contents_inline',)
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        ('Print', {
            'fields': ('issue', 'section',),
        }),
        ('Web', {
            'fields': ('pub_status', 'priority', 'slug', 'tags', 'show_ads',
                       'layout'),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        })
    )

    form = GalleryForm
    list_display = ('title', 'pk', 'section', 'pub_status',)
    list_filter = ('section',)

    class Media:
        css = {'all': ('css/admin/ImageGallery.css',)}

    def save_model(self, request, obj, form, change):
        contents = form.cleaned_data.pop('contents_inline', [])
        layout = form.cleaned_data.pop('layout', None)

        if obj.layout_instance is not None:
            if layout is None:
                obj.layout_instance.delete()
                obj.layout_instance = None
            else:
                obj.layout_instance.parent = layout
                obj.layout_instance.save()
        elif layout:
            obj.layout_instance = LayoutInstance.objects.create(
                parent=layout, name=obj.title[:50])

        super(GalleryAdmin, self).save_model(request, obj, form, change)
        # set the Gallery contents
        obj.contents.clear()

        for i, content in enumerate(contents):
            x = GalleryMembership(order=i, gallery=obj, content=content)
            x.save()
        # publish all the contents if the gallery is also publishe
        if int(obj.pub_status) == 1:  # why is pub_status a unicode?!
            for content in contents:
                if content.pub_status != 1:
                    content.pub_status = 1
                    content.save()
        return obj


class WidgetAdminForm(ContentModelForm):
    is_highcharts = forms.BooleanField(
        required=False,
        label='Uses Highcharts?')
    is_d3 = forms.BooleanField(
        required=False,
        label='Uses D3?')

    class Meta:
        model = Widget
        fields = '__all__'


class WidgetAdmin(ContentAdmin):
    list_display = ('title', 'pk', 'section', 'issue',
                    'pub_status',)
    list_display_links = ('title',)
    list_per_page = 30
    list_filter = ('section',)
    search_fields = ('title', 'description',)

    form = WidgetAdminForm

    fieldsets = (
        ('Image Setup', {
            'fields': ('title', 'html', 'javascript', 'is_highcharts', 'is_d3',
                       'description', 'pic'),
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        (' ', {
            'fields': ('issue', 'section',),
        }),
        ('Web', {
            'fields': ('pub_status', 'priority', 'slug', 'tags',),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        })
    )


class ContentTypeListFilter(admin.SimpleListFilter):
    title = 'content type'
    parameter_name = 'ctype'

    def lookups(self, request, model_admin):
        return [(t.name, t.name) for t in Content.types()]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        else:
            return queryset.filter(repr_type__name=self.value())


class ExternalContentForm(ContentModelForm):
    def __init__(self, *args, **kwargs):
        obj = kwargs.get('instance', None)
        if obj and obj.image:
            kwargs['initial'] = {'rel_content': str(obj.image.pk)}
        super(ExternalContentForm, self).__init__(*args, **kwargs)

    description = forms.fields.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': '5', 'cols': '67'}),
        help_text="""This is a description of the external content that will
                   appear as the teaser when displayed on the main
                   site.""", max_length=2500
    )
    subtitle = forms.fields.CharField(
        widget=forms.TextInput(attrs={'size': '100'}),
        required=False
    )
    title = forms.fields.CharField(
        widget=forms.TextInput(attrs={'size': '100'})
    )
    content_choices = reversed([(ct.pk, ct.name) for ct in Content.types()
                                if ct.name != 'external content'])
    repr_type = forms.TypedChoiceField(
        label='Content Type', choices=content_choices,
        coerce=lambda i: ContentType.objects.get(pk=i),
        required=True)
    redirect_url = forms.fields.CharField(
        widget=forms.TextInput(attrs={'size': '100'}))

    # this is put into ExternalContent.Image in
    # ExternalContentAdmin.save_model TODO implement limit in
    # RelatedContentField
    rel_content = RelatedContentField(
        label='Thumbnail Image', required=False,
        rel_types=[Image], limit=1)

    class Meta:
        model = ExternalContent
        fields = '__all__'


class ExternalContentAdmin(ContentAdmin):
    list_display = ('title', 'repr_type', 'pk', 'section', 'issue',
                    'pub_status',)
    search_fields = ('title',)
    list_filter = (ContentTypeListFilter, 'section',)

    fieldsets = (
        ('Info', {
            'fields': ('title', 'subtitle', 'repr_type',
                       'redirect_url', 'description',),
        }),
        ('Image', {
            'fields': ('rel_content',),
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        ('Print', {
            'fields': ('issue', 'section',),
        }),
        ('Web', {
            'fields': ('pub_status', 'priority', 'slug', 'tags',
                       'searchable',),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        })
    )

    form = ExternalContentForm
    ordering = ['-issue__issue_date']

    def get_queryset(self, request):
        if request.user.has_perm('content.delete_content'):
            qs = self.model._default_manager.all_objects()
        elif request.user.has_perm('content.content.can_publish'):
            qs = self.model._default_manager.admin_objects()
        else:
            qs = self.model._default_manager.draft_objects()

        return qs

    def get_form(self, request, obj=None):
        if not request.user.has_perm('content.make_unsearchable_content'):
            # make a copy for this request only
            self.fieldsets = tuple(self.fieldsets)
            for name, field_options in self.fieldsets:
                cleaned_fields = tuple(
                    f for f in field_options['fields'] if f != 'searchable')
                field_options['fields'] = cleaned_fields
        f = super(ExternalContentAdmin, self).get_form(request, obj)

        return f

    def has_change_permission(self, request, obj=None):
        u = request.user
        if u.is_superuser:
            return True
        if obj and int(obj.pub_status) != 0:
            return u.has_perm('content.content.can_publish')
        return super(ExternalContentAdmin, self).has_change_permission(
            request, obj)

    def save_model(self, request, obj, form, change):
        super(ExternalContentAdmin, self).save_model(
            request, obj, form, change)

        rel = form.cleaned_data.pop('rel_content', [])
        if len(rel) > 0:
            obj.image = rel[0].child
        else:
            obj.image = None
        obj.save()

        return obj


TEASER_RE = re.compile(r'<\s*\/?\w.*?>|{{{jump}}}')  # tags/jump tag


class ArticleForm(ContentModelForm):
    def __init__(self, *args, **kwargs):
        r = kwargs.get('instance', None)
        if r is not None:
            kwargs['initial'] = {
                'rel_content_inline': r.rel_admin_content,
                'rec_articles_inline': r.rec_articles_admin
            }
            if r.layout_instance:
                kwargs['initial']['layout'] = r.layout_instance.parent
        super(ArticleForm, self).__init__(*args, **kwargs)

    title = forms.fields.CharField(
        label='Headline',
        required=True, widget=forms.TextInput(attrs={'size': '100'}))
    subtitle = forms.fields.CharField(
        label='Subheadline',
        required=False, widget=forms.TextInput(attrs={'size': '100'}))
    description = forms.fields.CharField(
        label='Teaser',
        required=False,
        widget=forms.Textarea(attrs={'rows': '5', 'cols': '67'}),
        help_text="""
        A short sample from the article, or a summary of the article. <br>
        If you don't provide a teaser, we will automatically generate one
        for you.""", max_length=2500
    )
    text = forms.fields.CharField(
        widget=WYSIWYGEditor()
    )
    multimedia_contributors = ContributorChoicesField(required=False)
    corrections = forms.ModelChoiceField(
        queryset=Section.objects.all(), required=False)
    layout = forms.ModelChoiceField(
        queryset=Layout.objects.filter(article_template=True),
        required=False, empty_label='Default')
    parent_topic = forms.ModelChoiceField(
        queryset=TopicPage.objects.admin_objects().order_by('-created_on'),
        empty_label='Default', required=False)

    rel_content_inline = RelatedContentField(
        label='New admin content', required=False,
        rel_types=[Image, Gallery, Article, Map, FlashGraphic, Video, Widget])
    rec_articles_inline = RelatedContentField(
        label='Recommended articles.', required=False,
        rel_types=[Article])

    def clean_description(self):
        """Add a teaser if one does not exist."""
        description = self.cleaned_data.get('description')
        has_jump = Article.JUMP_REGEX.search(self.cleaned_data.get('text'))
        if not (description or has_jump):
            raise forms.ValidationError(
                'Must specify either teaser text or include a page break in '
                'article text.')
        return description

    def clean(self):
        self.cleaned_data.pop('corrections')
        return super(ArticleForm, self).clean()

    class Meta:
        model = Article
        fields = '__all__'


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        opponent = cleaned_data.get('opponent')
        their_score = cleaned_data.get('their_score')
        our_score = cleaned_data.get('our_score')
        text = cleaned_data.get('text')

        if ((opponent == '' or their_score == '' or our_score == '') and
                (text == '')):
            raise forms.ValidationError(
                'Sports scores need text or scores filled in to be valid')

        # Always return the full collection of cleaned data.
        return cleaned_data


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 1
    form = ScoreForm
    fields = ('sport', 'opponent', 'our_score', 'their_score', 'text',
              'event_date', 'home_game',)


class ArticleAdmin(ContentAdmin):
    list_display = ('title', 'section', 'issue', 'pub_status',
                    'group',)
    search_fields = ('title', 'slug')
    list_filter = ('section', LimitedIssueListFilter, )
    readonly_fields = ('shortcodes_link',)

    raw_fieldsets = (
        ('Headline', {
            'fields': ('title', 'subtitle',),
        }),
        ('Text', {
            'fields': ('text', 'shortcodes_link', 'description',),
        }),
        ('Byline', {
            'fields': ('contributors', 'multimedia_contributors',
                       'byline_type', 'tagline', 'contributor_override'),
        }),
        ('Print', {
            'fields': ('issue', 'section', 'page',),
        }),
        ('Related Content', {
            'fields': ('rel_content_inline',),
        }),
        ('Web', {
            'fields': ('pub_status', 'parent_topic', 'priority', 'slug',
                       'tags', 'layout', 'searchable', 'paginate', 'show_ads'),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        }),
        ('Recommended Articles', {
            'fields': ('rec_articles_inline',),
        }),
    )

    form = ArticleForm
    ordering = ['section__id']

    def shortcodes_link(self, instance):
        return mark_safe('<a target="_blank" href="https://docs.google.com/a/th'
                         'ecrimson.com/document/d/1HW4nnqLzkEoh1gN4AfnYgpYDLw8w'
                         'PV1B3GaAK7fhASA/">Click Here</a>')
    shortcodes_link.allow_tags = True
    shortcodes_link.short_description = 'Shortcodes Documentation'

    class Media:
        js = (
            'scripts/jquery.js',
        )

    def get_queryset(self, request):
        if request.user.has_perm('content.delete_content'):
            qs = self.model._default_manager.all_objects()
        elif request.user.has_perm('content.content.can_publish'):
            qs = self.model._default_manager.admin_objects()
        else:
            qs = self.model._default_manager.draft_objects()
        # if it's the top level (no filters, no search parameter),
        # return None - force the user to choose an issue or
        # (this avoids the super-inefficient sort)
        if (request.path.strip('/').rstrip('/')[-7:] == 'article' and
                (request.GET.get('issue__id__exact', '') == '') and
                (request.GET.get('q', '') == '') and
                (request.GET.get('limitedissue', '') == '')):
            return qs.none()
        return qs

    def get_form(self, request, obj=None):
        # make a copy for this request only
        self.fieldsets = copy.deepcopy(self.raw_fieldsets)
        if not request.user.has_perm('content.make_unsearchable_content'):
            for name, field_options in self.fieldsets:
                cleaned_fields = tuple(
                    f for f in field_options['fields'] if f != 'searchable')
                field_options['fields'] = cleaned_fields
        f = super(ArticleAdmin, self).get_form(request, obj)
        if obj is not None:
            f.base_fields['corrections'].widget.choices = tuple(
                [(x, x.pk) for x in Correction.objects.filter(article=obj)])
        else:
            f.base_fields['corrections'].widget.choices = []

        return f

    def has_change_permission(self, request, obj=None):
        u = request.user
        if u.is_superuser:
            return True
        # cannot make change to published stuff; must use corrections interface
        if obj and int(obj.pub_status) != 0:
            return u.has_perm('content.content.can_publish')
        return super(ArticleAdmin, self).has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        rel = form.cleaned_data.pop('rel_content_inline', [])

        layout = form.cleaned_data.pop('layout', None)

        if obj.layout_instance is not None:
            if layout is None:
                obj.layout_instance.delete()
                obj.layout_instance = None
            else:
                obj.layout_instance.parent = layout
                obj.layout_instance.save()
        elif layout:
            obj.layout_instance = LayoutInstance.objects.create(
                parent=layout, name=obj.title[:50])

        super(ArticleAdmin, self).save_model(request, obj, form, change)

        obj.rel_content.clear()
        for i, r in enumerate(rel):
            x = ArticleContentRelation(order=i, article=obj, related_content=r)
            x.save()

        # save new recommended articles
        obj.rec_articles.clear()
        obj.rec_articles = [c.child for c in form.cleaned_data.pop(
            'rec_articles_inline', [])]
        obj.save()

        shortcode_ids = Article.extract_shortcoded_content(
            form.cleaned_data.get('text', ''))
        first_order = len(rel)
        for i, rid in enumerate(shortcode_ids):
            try:
                r = Content.objects.get(pk=rid)
                if r not in rel:
                    x = ArticleContentRelation(
                        order=(i + first_order),
                        article=obj, related_content=r)
                    x.shortcoded = True
                    x.save()
                else:
                    x = ArticleContentRelation.objects.get(
                        article=obj, related_content=r.child)
                    x.shortcoded = True
                    x.save()
            except:
                pass

        # publish all the contents if the gallery is also published
        if int(obj.pub_status) != 0:  # why is pub_status a unicode?!
            for content in rel:
                if content.pub_status != 1:
                    content.pub_status = 1
                    content.save()

        # Notifies authority figures if an old article has been
        # modified, otherwise we'd never notice
        notify_settings = settings.NOTIFY_ON_SKETCHY_EDIT
        suspicion_cutoff = date.today() - timedelta(
            days=notify_settings['time_span'])
        if (obj.issue.issue_date < suspicion_cutoff and
                notify_settings['enabled']):
            subject = notify_settings['subject']
            body = render_to_string('email/suspicious.txt', {'article': obj})
            send_mail(subject, body, notify_settings['from'],
                      notify_settings['to'], fail_silently=False)

        # Force Facebook to rescrape the article page.
        if obj.pub_status != 0:
            # Delay a few seconds, or Facebook will request the article before
            # the database has updated and clog the cache with the old version.
            purge_facebook.apply_async(args=[obj.get_full_url()], countdown=5)

        return obj

    def get_urls(self):
        urls = super(ArticleAdmin, self).get_urls()
        urls = [
            url(r'^rel_content/get/(?P<obj_id>\d+)/$',
                self.admin_site.admin_view(self.get_rel_content)),
            url(r'^rel_content/get/(?P<obj_id>\d+)/$',
                self.admin_site.admin_view(self.get_rel_content)),
            url(r'^rel_content/find/',
                self.admin_site.admin_view(self.find_rel_content)),
            url(r'^rel_content/suggest/(\d+)/([\d,]*)/(\d+)/$',
                self.admin_site.admin_view(self.suggest_rel_content)),
            url(r'^(?P<article_id>\d+)/preview/$',
                self.admin_site.admin_view(self.preview_page)),
            url(r'^(?P<article_id>\d+)/create_layout_instance/$',
                self.admin_site.admin_view(self.create_layout_instance)),
        ] + urls
        return urls

    def create_layout_instance(self, request, article_id):
        try:
            inst = LayoutInstance.objects.create(
                parent=Layout.objects.all()[0], active=True)
            a = Article.objects.all_objects().get(pk=article_id)
            a.layout_instance = inst
            a.save()
            return HttpResponseRedirect(reverse(
                'admin:placeholders_layoutinstance_change', args=[inst.pk]))
        except:
            raise Http404

    def preview_page(self, request, article_id):
        try:
            a = Article.objects.all_objects().get(pk=article_id)
            return a._render_to_response('page', request=request)
        except:
            raise Http404

    def get_rel_content(self, request, obj_id):
        """
        returns HTML with a Content obj rendered as 'admin.line_item'
        @obj_id : Content pk
        """

        r = get_object_or_404(Content.objects.admin_objects(), pk=int(obj_id))
        json_dict = {
            'html': mark_safe(r._render('admin.line_item')),
        }
        return HttpResponse(json.dumps(json_dict))

    def find_rel_content(self, request):
        """returns JSON containing Content objects and pg numbers"""
        if request.method != 'GET':
            raise Http404

        ct_ids = [int(x) for x in
                  request.GET.get('ct_id', '0').rstrip(';').split(';')]
        st_dt = request.GET.get('st_dt', date.today().strftime('%m/%d/%Y'))
        end_dt = request.GET.get(
            'end_dt', (date.today() - timedelta(days=7)).strftime('%m/%d/%Y'))
        q = request.GET.get('q', '')
        page = request.GET.get('page', 1)

        OBJS_PER_REQ = 16
        if ct_ids != [0]:
            type_filt = Q(content_type__pk__in=ct_ids)
        else:
            type_filt = Q()
        st_dt = datetime.strptime(st_dt, '%m/%d/%Y')
        end_dt = datetime.strptime(end_dt, '%m/%d/%Y')

        # Cache results
        key = ''.join(map(str, ct_ids))
        key = '_'.join([
            key, q, st_dt.strftime('%Y-%m-%d'), end_dt.strftime('%Y-%m-%d')])
        key = 'find_rel_content.' + hashlib.md5(key).hexdigest()

        objs = cache.get(key)
        if not objs:
            objs = Content.objects.admin_objects(
                start=st_dt,
                end=end_dt).filter(
                Q(title__icontains=q) | Q(slug__icontains=q)).filter(type_filt)
            cache.set(key, objs, settings.CACHE_SHORT)
        p = Paginator(objs, OBJS_PER_REQ).page(page)

        json_dict = {}
        json_dict['objs'] = []

        # This is rather messily done.  Content_thumbnail is unneeded,
        # should just call render to admim.thumbnail instead
        for obj in p.object_list:
            html = render_to_string('content_thumbnail.html', {'objs': [obj]})
            json_dict['objs'].append([obj.pk, html])
        json_dict['next_page'] = p.next_page_number() if p.has_next() else 0
        json_dict['prev_page'] = p.previous_page_number() \
            if p.has_previous() else 0

        return HttpResponse(json.dumps(json_dict))

    def suggest_rel_content(self, request, ct_id, tags, page):
        """
        returns JSON containing Content objects and pg numbers
        """
        OBJS_PER_REQ = 3

        # intersection between multiple lists using reduce
        def intersect(lists):
            return list(reduce(set.intersection, (set(l) for l in lists)))

        # can't really suggest if they don't give you any tags
        if tags == '':
            json_dict = {}
            json_dict['objs'] = []
            return HttpResponse(json.dumps(json_dict))

        tags = tags.split(',')
        tagarticles = []
        newerthan = date.today() + timedelta(days=-365)
        for tag in tags:
            # Filter by content type ID only if they didn't search for
            # all types of content
            if ct_id == '0':
                tagarticles.append(Content.objects.filter(
                    issue__issue_date__gte=newerthan).filter(tags__pk=tag))
            else:
                tagarticles.append(Content.objects.filter(
                    issue__issue_date__gte=newerthan)
                    .filter(content_type__pk=ct_id).filter(tags__pk=tag))

        objstemp = []
        # Iterate through from most to least matches on tags
        for i in range(len(tagarticles), 0, -1):
            combs = combinations(tagarticles, i)
            for comb in combs:
                inter = (intersect(comb))
                for inte in inter:
                    if inte not in objstemp:
                        objstemp.append(inte)

        objs = []
        for o in objstemp:
            objs.append(o)

        p = Paginator(objs, OBJS_PER_REQ).page(page)

        json_dict = {}
        json_dict['objs'] = []
        for obj in p.object_list:
            html = render_to_string('content_thumbnail.html', {'objs': [obj]})
            json_dict['objs'].append([obj.pk, html])
        json_dict['next_page'] = p.next_page_number() if p.has_next() else 0
        json_dict['prev_page'] = p.previous_page_number() \
            if p.has_previous() else 0
        return HttpResponse(json.dumps(json_dict))


class ReviewForm(forms.ModelForm):
    article = forms.IntegerField(
        required=True, help_text='The article id'
        'of the article the review is attached to. This is the number in '
        'the URL on the admin page. Ie. URL=/admin/content/article/2331/ '
        '=> Article ID = 2331.', label='Article ID')

    class Meta:
        model = Review
        fields = '__all__'

    def clean_article(self):
        a = self.cleaned_data['article']
        try:
            a = Article.objects.get(pk=int(a))
        except ValueError, Article.DoesNotExist:
            raise forms.ValidationError('Article with that id does not exist.')
        return a


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm
    radio_fields = {'rating': admin.HORIZONTAL}


class VideoForm(ContentModelForm):
    pic = forms.fields.ImageField(
        widget=admin.widgets.AdminFileWidget,
        required=False, help_text="If you leave this blank, we'll use "
        'the default screenhshot genereated by Youtube.')
    gen_pic = forms.fields.BooleanField(
        label='Check this box if '
        'you want to regenerate the preview image.', required=False)

    def clean_key(self):
        # try to filter out keys that are probably wrong
        key = self.cleaned_data['key']
        if key.find('watch?v=') is not -1:
            key = key[key.find('watch?v=') + 8:]
        if key.find('&') is not -1:
            key = key[:key.find('&')]
        return key

    class Meta:
        model = Video
        fields = '__all__'


class VideoAdmin(ContentAdmin):
    form = VideoForm
    list_filter = ('section',)
    list_display = ('admin_thumb', 'title', 'youtube_url', 'section',
                    'issue', 'pub_status',)
    list_display_links = ('admin_thumb', 'title',)

    fieldsets = (
        ('Video Setup', {
            'fields': ('title', 'description', 'key', 'pic', 'gen_pic'),
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        ('Publishing', {
            'fields': ('issue', 'section', 'pub_status', 'priority', 'slug',
                       'tags', 'show_ads',),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        })
    )

    def save_model(self, request, obj, form, change):
        # if gen_pic is set, or there is no picture on the obj / form
        if (form.cleaned_data['pic'] and not
            form.cleaned_data['gen_pic'] and
                form.initial['key'] == form.cleaned_data['key']):
            return super(VideoAdmin, self).save_model(
                request, obj, form, change)

        img_url = 'https://img.youtube.com/vi/' + obj.key + '/0.jpg'
        super(VideoAdmin, self).save_model(request, obj, form, change)

        try:
            img = urllib.urlretrieve(img_url)
            i = pilImage.open(img[0])
            arrow = pilImage.open(
                settings.STATIC_MAIN + '/images/video-button.png')

            fpath = youtube_get_save_path(obj, img_url.rsplit('/', 1)[1])
            # auto-crop the image
            i = i.crop((124, 50, 464, 305))
            i.paste(arrow, arrow)
            i.save(img[0])

            f = File(open(img[0]))

            obj.pic.save(fpath, f)
            obj.save()
            f.close()
            os.remove(img[0])
        except:
            messages.error(
                request, 'There was a problem automatically'
                ' downloading the preview image from Youtube (this may happen '
                'if you just finished uploading the video to Youtube).  You '
                'should add a preview image manually, or resave this video '
                'later.')
            return obj

        return obj


class FlashGraphicForm(ContentModelForm):
    def __init__(self, *args, **kwargs):
        super(FlashGraphicForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FlashGraphic
        fields = '__all__'


class FlashGraphicAdmin(ContentAdmin):
    form = FlashGraphicForm

    fieldsets = (
        ('Graphic Setup', {
            'fields': ('graphic', 'pic', 'title', 'description', 'width',
                       'height'),
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        ('Publishing', {
            'fields': ('issue', 'section', 'pub_status', 'priority', 'slug',
                       'tags',),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        })
    )


class TableForm(ContentModelForm):
    class Meta:
        model = Table
        fields = '__all__'


class TableAdmin(ContentAdmin):
    list_display = ('title', 'pk', 'section', 'issue',
                    'pub_status')
    list_display_links = ('title',)
    list_per_page = 30
    list_filter = ('section',)
    search_fields = ('title', 'description',)

    form = TableForm

    fieldsets = (
        ('Table Setup', {
            'fields': ('title', 'csv_file', 'json_file_link', 'description'),
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        ('Publishing', {
            'fields': ('issue', 'section', 'pub_status', 'priority', 'slug',
                       'tags',),
        }),
    )
    readonly_fields = ('json_file_link',)

    def json_file_link(self, obj):
        return '<a href="%s">%s</a>' % (obj.json_file.url, obj.json_file)
    json_file_link.allow_tags = True
    json_file_link.short_description = 'JSON file'

    def save_model(self, request, obj, form, change):
        if 'csv_file' in form.changed_data:
            obj.update_json()
        super(TableAdmin, self).save_model(request, obj, form, change)


class MarkerInline(admin.TabularInline):
    model = Marker
    extra = 3
    fields = ('popup_text', 'lat', 'lng', 'color')


class MapForm(ContentModelForm):
    map_preview = MapBuilderField(label='Map Preview', required=False)
    marker_import_file = forms.fields.FileField(
        required=False,
        help_text=string_concat(
            'A CSV from which to batch import map markers.',
            ' <a href="',
            reverse_lazy(
                'admin:sample_marker_import_file'), '">Download sample</a>.'))

    class Meta:
        model = Map
        fields = '__all__'


class MapAdmin(ContentAdmin):
    search_fields = ('title', 'description',)
    form = MapForm

    inlines = [MarkerInline]

    fieldsets = (
        ('Details', {
            'classes': ('frozen', 'collapse'),
            'fields': ('zoom_level', 'center_lng', 'center_lat',
                       'display_mode',),
        }),
        ('Contributors', {
            'fields': ('contributors',),
        }),
        ('Organization', {
            'fields': ('section', 'pub_status', 'issue', 'slug', 'tags',
                       'priority',),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        }),
        ('Map Setup', {
            'fields': ('title', 'description', 'map_preview'),
        }),
        ('Batch Import Markers', {
            'fields': ('marker_import_file',)
        })
    )

    def get_urls(self):
        return [
            url(r'^sample_marker_import_file/$',
                self.admin_site.admin_view(
                    self.sample_marker_import_file, cacheable=True),
                name='sample_marker_import_file')
        ] + super(MapAdmin, self).get_urls()

    def sample_marker_import_file(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="map_import.csv"'

        writer = csv.writer(response)
        writer.writerow(['lat', 'lng', 'address', 'color', 'popup_text'])
        writer.writerow(['42.3722893', '-71.119688', '', 'red', 'Shake Shack'])
        writer.writerow([
            '', '', 'Harvard Square', 'red',
            'Leave out `lat` and `lng` to automatically geocode `address`'])
        writer.writerow([
            '', '', '', '',
            'Valid colors: ' + ', '.join(Marker.valid_colors())])

        return response

    class Media:
        js = (
            'js/lib/papaparse.js',
            'scripts/admin/marker_import.js',
        )


class SectionAdminForm(ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

    def clean(self):
        return super(SectionAdminForm, self).clean()


class SectionLayoutInline(admin.StackedInline):
    model = Section.layout_instances.through
    verbose_name = 'Layout Instance'
    fields = ('layoutinstance', 'active', 'admin_link',)
    readonly_fields = ('admin_link',)
    extra = 0

    def admin_link(self, instance):
        obj = instance.layoutinstance
        f = (obj._meta.app_label, obj._meta.model_name)
        url = reverse('admin:%s_%s_change' % f, args=[obj.id])
        return mark_safe(u'<a target="_blank" href="{u}">Edit</a>'
                         .format(u=url))
    admin_link.allow_tags = True
    admin_link.short_description = 'Admin Link'


class SectionAdmin(admin.ModelAdmin):
    fields = ('name', 'can_have_articles',)
    readonly_fields = ('name', 'can_have_articles',)
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 30

    form = SectionAdminForm

    inlines = [SectionLayoutInline, ]

    def get_queryset(self, request):
        return Section.all_objects.all()

    def save_model(self, request, obj, form, change):
        if change:
            expire_page(obj.get_absolute_url())

        super(SectionAdmin, self).save_model(request, obj, form, change)

    class Media:
        js = (
            'scripts/admin/placeholders.js',
        )


class IndexLayoutInline(admin.StackedInline):
    model = Index.layout_instances.through
    verbose_name = 'Layout Instance'
    fields = ('layoutinstance', 'active', 'admin_link',)
    readonly_fields = ('admin_link',)
    extra = 0

    def admin_link(self, instance):
        obj = instance.layoutinstance
        f = (obj._meta.app_label, obj._meta.model_name)
        url = reverse('admin:%s_%s_change' % f, args=[obj.id])
        return mark_safe(u'<a target="_blank" href="{u}">Edit</a>'
                         .format(u=url))
    admin_link.allow_tags = True
    admin_link.short_description = 'Admin Link'


class IndexAdmin(SingletonModelAdmin):
    exclude = ('layout_instances',)
    inlines = [IndexLayoutInline, ]

    class Media:
        js = (
            'scripts/admin/placeholders.js',
        )

    def save_model(self, request, obj, form, change):
        super(IndexAdmin, self).save_model(request, obj, form, change)
        cache_homepage.apply_async()


class TopicPageAdminForm(ContentModelForm):
    def __init__(self, *args, **kwargs):
        obj = kwargs.get('instance', None)
        if obj and obj.image:
            kwargs['initial'] = {'rel_content': str(obj.image.pk)}
        super(TopicPageAdminForm, self).__init__(*args, **kwargs)

    parent = TopicPageSingleChoiceField(required=False)
    delete_parent = forms.BooleanField(
        initial=False, required=False, label='Clear parent')

    rel_content = RelatedContentField(
        label='Thumbnail Image', required=False,
        rel_types=[Image], limit=1)

    """
    TODO
    Stupid hack. I don't know the right way to fix this
    Django checks if the parent exists using the default manager, rather than
    the admin manager. Temporarily switch out the default queryset.
    """
    def full_clean(self):
        orig = TopicPage.objects.get_queryset
        TopicPage.objects.get_queryset = TopicPage.objects.admin_objects
        ret = super(TopicPageAdminForm, self).full_clean()
        TopicPage.objects.get_queryset = orig
        return ret

    def clean(self):
        if ('delete_parent' in self.cleaned_data and
                self.cleaned_data['delete_parent']):
            self.cleaned_data['parent'] = None
        return super(TopicPageAdminForm, self).clean()

    class Meta:
        model = TopicPage
        fields = '__all__'


class TopicPageAdmin(ContentAdmin):
    form = TopicPageAdminForm
    readonly_fields = ('admin_link',)

    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description', 'admin_link',
                       'parent', 'delete_parent', 'pos'),
        }),
        ('Byline', {
            'fields': ('contributors',),
        }),
        ('Print', {
            'fields': ('issue', 'section',),
        }),
        ('Web', {
            'fields': ('pub_status', 'rel_content', 'priority', 'slug',
                       'tags'),
        }),
        ('Grouping', {
            'fields': ('group', 'delete_group'),
            'classes': ('collapse',),
        })
    )

    def admin_link(self, instance):
        obj = instance.layout_instance
        f = (obj._meta.app_label, obj._meta.model_name)
        url = reverse('admin:%s_%s_change' % f, args=[obj.id])
        return mark_safe(u'<a target="_blank" href="{u}">Edit</a>'
                         .format(u=url))
    admin_link.allow_tags = True
    admin_link.short_description = 'LayoutInstance Admin Link'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.layout_instance = LayoutInstance.objects.create(
                name=unicode(obj),
                parent=Layout.objects.get(name=obj.get_default_layout()))

        # prevent changing parent of published TopicPage as that changes
        # the slug
        new_status = int(obj.pub_status)
        if change:
            old_obj = self.model.objects.all_objects().get(pk=obj.pk)
            old_status = int(obj.original_pub_status)
        else:
            old_status = None

        if (old_status == 1 and new_status == 1 and
                (old_obj.parent != obj.parent)):
            messages.add_message(
                request, messages.INFO, 'You can\'t change '
                'the parent on published TopicPages because this changes '
                'the slug. Changes to this field have been undone.')
            obj.parent = old_obj.parent

        # prevent forming loops via the parent relationship
        if change:
            parent = obj.parent
            pk_set = set([obj.pk])

            while parent:
                # if we've already encountered this TopicPage, raise and
                # undo changes
                if parent.pk in pk_set:
                    messages.add_message(
                        request, messages.INFO, 'You can\'t form a loop '
                        'with the parent field. Please examine the parent'
                        'hierarchy. Changes to the parent field have '
                        'been undone.')
                    obj.parent = old_obj.parent
                    parent = None
                else:
                    pk_set.add(parent.pk)
                    parent = parent.parent

        super(TopicPageAdmin, self).save_model(request, obj, form, change)

        rel = form.cleaned_data.pop('rel_content', [])
        if len(rel) > 0:
            obj.image = rel[0].child
        else:
            obj.image = None
        obj.save()

        return obj

    def get_urls(self):
        urls = [
            url(r'^(?P<topicpage_id>\d+)/preview/$',
                self.admin_site.admin_view(self.preview_page)),
        ] + super(TopicPageAdmin, self).get_urls()
        return urls

    def preview_page(self, request, topicpage_id):
        try:
            t = TopicPage.objects.all_objects().get(id=topicpage_id)
        except (TopicPage.DoesNotExist, ValueError):
            raise Http404

        data = {'topic': t, 'nav': t.section.name.lower()}
        return t.layout_instance.render(request, data)


class FeaturePackageForm(forms.ModelForm):

    title = forms.fields.CharField(
        widget=forms.TextInput(attrs={'size': '70'}),
        required=True, max_length=250
    )

    pub_status = forms.ChoiceField(
        FeaturePackage.PUB_CHOICES, required=True,
        label='Published Status', help_text='Only execs can publish content.'
    )

    description = forms.fields.CharField(
        widget=forms.Textarea(attrs={'rows': '5', 'cols': '67'}),
        required=True, help_text="""
        Please provide a short description of the package""", max_length=2500
    )

    feature = forms.fields.BooleanField(
        label='Check this box if you want the banner image to be displayed on '
        'the front page for this package.', required=False)

    banner = forms.fields.ImageField(
        widget=admin.widgets.AdminFileWidget,
        required=False, label='Banner',
        help_text='Only images that are 550px wide')

    now = datetime.now()
    dateField = forms.fields.DateField(
        initial=str(now.month) + '/' + str(now.day) + '/' + str(now.year),
        label='Slug Date',
        help_text='This is used to generate the slug',
        input_formats=['%m/%d/%Y'])

    model = FeaturePackage

    class Meta:
        model = FeaturePackage
        fields = '__all__'


class FeaturePackageSectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        r = kwargs.get('instance', None)
        if r is not None:
            kwargs['initial'] = {'related_content_form': r.rel_admin_content}
        super(FeaturePackageSectionForm, self).__init__(*args, **kwargs)

    model = FeaturePackageSection

    related_content_form = RelatedContentField(
        label='Contents', required=False,
        rel_types=[Image, Gallery, Article, Map, FlashGraphic, Video])

    def has_changed(self):
        return True

    class Media:
        js = (
            'scripts/admin/FeaturePackage.js',
        )

    class Meta:
        model = FeaturePackageSection
        fields = '__all__'


class FeaturePackageSectionInline(admin.StackedInline):
    model = FeaturePackageSection
    form = FeaturePackageSectionForm
    extra = 0


class FeaturePackageAdmin(admin.ModelAdmin):
    form = FeaturePackageForm
    inlines = [FeaturePackageSectionInline]

    list_display = ('title', 'feature', 'pub_status',)
    search_fields = ('title',)

    def save_formset(self, request, form, formset, change):
        if formset.model != FeaturePackageSection:
            return super(FeaturePackageAdmin, self).save_formset(
                request, form, formset, change)

        instances = formset.save(commit=False)
        counter = 0
        for inst in instances:
            inst.save()
            section = inst
            contents = formset.forms[counter] \
                              .cleaned_data['related_content_form']
            section.related_contents.clear()
            for x, r in enumerate(contents):
                d = PackageSectionContentRelation(
                    order=x, FeaturePackageSection=section, related_content=r)
                d.save()

            counter += 1


class BreakingNewsAdmin(SingletonModelAdmin):
    pass


class GenericFileAdmin(admin.ModelAdmin):
    pass


class CorrectionAdmin(admin.ModelAdmin):
    pass
