import json
import logging
import os

from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .models import LayoutInstance, Placeholder, PlaceholderContentRelation

from crimsononline.content.forms import RelatedContentField, TagSelectWidget
from crimsononline.content.models import (
    Article, ExternalContent, FlashGraphic, Gallery, Image, Map, Tag,
    TopicPage, Video)

TEMPLATES_DIR = 'crimsononline/placeholders/templates/'

logger = logging.getLogger(__name__)


class PlaceholderForm(forms.ModelForm):

    content_form = RelatedContentField(
        label='Contents',
        required=False,
        rel_types=[Image, Gallery, Article, Map,
                   FlashGraphic, Video, ExternalContent, TopicPage])

    autofill_tags = forms.ModelMultipleChoiceField(
        Tag.objects.all(), required=False,
        widget=TagSelectWidget('Tags', False, tag_qs=Tag.objects.all()),
    )

    def __init__(self, *args, **kwargs):
        r = kwargs.get('instance', None)
        if r is not None:
            kwargs['initial'] = {'content_form': r.rel_admin_content}
        super(PlaceholderForm, self).__init__(*args, **kwargs)
        if r is not None and r.node is not None:
            cts = [ContentType.objects.get(app_label='content',
                                           model=c.replace(' ', ''))
                   for c in r.valid_types()]
            self.fields['content_form'].widget.rel_types = [ct.model_class()
                                                            for ct in cts]
            self.fields['autofill_contenttypes'].queryset = \
                ContentType.objects.filter(pk__in=[ct.pk for ct in cts])

    def clean(self):
        length = len(self.cleaned_data['content_form'])
        if (self.instance.node and
                self.instance.node.content_range['max'] < length):
            self._errors['content_form'] = ErrorList(
                [mark_safe('Placeholder can only hold %d items.' %
                 self.instance.node.content_range['max'])])
        return self.cleaned_data

    class Meta:
        model = Placeholder
        fields = '__all__'


class PlaceholderInline(admin.StackedInline):
    form = PlaceholderForm
    model = Placeholder
    extra = 0
    max_num = 0
    ordering = ('position',)
    fields = ('title', 'title_link', 'min_items', 'max_items', 'position',
              'extra_text', 'autofill_tags', 'autofill_section',
              'autofill_number', 'autofill_prioritize', 'autofill_contenttypes',
              'require_media', 'content_form')
    readonly_fields = ('min_items', 'max_items')

    def get_formset(self, request, instance=None, **kwargs):
        """
        Ensures that all of the placeholders that have been defined in a
        template have been created before the admin form is rendered
        """
        if instance:
            instance.save()

        parent = super(PlaceholderInline, self)
        return parent.get_formset(request, instance, **kwargs)

    def max_items(self, instance):
        if instance.node:
            return instance.node.content_range['max']
        else:
            return None

    class Meta:
        model = Placeholder


class LayoutInstanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LayoutInstanceForm, self).__init__(*args, **kwargs)

    model = LayoutInstance

    class Meta:
        model = LayoutInstance
        fields = '__all__'


class LayoutInstanceAdmin(admin.ModelAdmin):
    form = LayoutInstanceForm
    inlines = [PlaceholderInline]
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('template_path',)

    def template_path(self, obj):
        return obj.parent.template_path

    def get_urls(self):
        urls = super(LayoutInstanceAdmin, self).get_urls()
        return urls

    def list_layouts(request):
        templates = os.listdir('crimsononline/placeholders/templates/')
        templates = [f for f in templates if os.path.isfile(f)]
        return HttpResponse(json.dumps(templates),
                            content_type='application/json')

    def save_formset(self, request, form, formset, change):
        if formset.model != Placeholder:
            return super(LayoutInstanceAdmin, self).save_formset(
                request, form, formset, change)
        else:
            valid_names = set(p.name
                              for p in form.instance.defined_placeholders())
            for f in formset.forms:
                if f.instance.name not in valid_names:
                    f.instance.delete()
                elif not f.cleaned_data['DELETE']:
                    inst = f.instance
                    inst.save()
                    contents = f.cleaned_data['content_form']
                    inst.content_relations.all().delete()
                    for x, r in enumerate(contents):
                        d = PlaceholderContentRelation(position=x,
                                                       placeholder=inst,
                                                       content=r.child)
                        d.save()
            formset.save()
