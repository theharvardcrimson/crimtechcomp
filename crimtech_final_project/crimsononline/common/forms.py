"""
Form form things that would be useful across apps and models.
This probably means only form widgets and form fields.
"""

import logging
import re

from django import forms
from django.db.models import Q
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django_select2 import (
    AutoHeavySelect2TagWidget, AutoModelSelect2Field,
    AutoModelSelect2MultipleField, AutoModelSelect2TagField)

from crimsononline.archive_photos.models import ArchiveCategory
from crimsononline.content.models import (
    ContentGroup, ContentType, Contributor, TopicPage)

logger = logging.getLogger(__name__)


class JSTreeWidget(forms.widgets.HiddenInput):
    allow_multiple_selected = False

    def __init__(self, attrs=None, model=ArchiveCategory):
        super(JSTreeWidget, self).__init__(attrs)

        self.model = model

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        if 'class' not in attrs:
            attrs['class'] = 'jstree'
        else:
            attrs['class'] += ' jstree'

        final_attrs = self.build_attrs(attrs, name=name)
        output = []
        output.append(format_html('<div{0}>', flatatt(final_attrs)))

        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</div>')
        hidden = super(JSTreeWidget, self).render(name, value, attrs)
        output.append(hidden)

        output.append('<script>$(document).ready(function(){{$("div#{0}").'
                      'jstree(true).select_node("{1}");}});</script>'
                      .format(attrs['id'], value))

        return mark_safe('\n'.join(output))

    def render_rec(self, cat_set):
        output = []

        if cat_set:
            output.append('<ul>')
            for cat in cat_set:
                output.append(
                    format_html(
                        '<li id="{1}">{2}',
                        ContentType.objects.get_for_model(cat).model,
                        cat.pk, cat.name))
                children = self.render_rec(cat.children.all())
                if children:
                    output.extend(children)
                output.append('</li>')
            output.append('</ul>')

        return output

    def render_options(self, choices, selected_choices):
        output = self.render_rec(self.model.objects.filter(parent=None))
        return '\n'.join(output)

    def clean(self, value):
        logger.debug(value)
        if value:
            obj = self.model.objects.get(pk=int(value))
            logger.debug(obj)
            return obj
        else:
            return None

    class Media:
        js = (
            'lib/jstree/jstree.min.js',
            'js/jstree-widget.js',
        )
        css = {
            'all': ('lib/jstree/themes/default/style.min.css',)
        }


class ContributorChoicesField(AutoModelSelect2MultipleField):
    queryset = Contributor.objects.filter(is_active=True)
    search_fields = [
        'first_name__icontains',
        'middle_name__icontains',
        'last_name__icontains'
    ]
    empty_values = ['']

    def prepare_qs_params(self, request, search_term, search_fields):
        search_terms = search_term.split()

        or_queries = Q()
        for term in search_terms:
            term_query = Q()
            for field in search_fields:
                term_query |= Q(**{field: term})
            or_queries &= term_query

        return {'or': [or_queries], 'and': {}}

    def security_check(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            return True
        else:
            return False


class ContributorTagWidget(AutoHeavySelect2TagWidget):
    def init_options(self):
        super(ContributorTagWidget, self).init_options()
        self.options['tokenSeparators'] = [',', ';']


class ContributorChoicesAddField(AutoModelSelect2TagField):
    widget = ContributorTagWidget
    queryset = Contributor.objects.filter(is_active=True)
    search_fields = ['first_name__icontains', 'last_name__icontains']
    empty_values = ['']
    splitter = re.compile('(?P<first>[\w ]+|\w\.) ((?P<middle>[\w]+\.) '
                          '(?P<last1>[\w\. ]+)|(?P<last2>[\w\.]+))')

    def security_check(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            return True
        else:
            return False

    def get_model_field_values(self, value):
        m = self.splitter.match(value)
        try:
            ret = {'first_name': m.group('first'),
                   'middle_name': m.group('middle') or '',
                   'last_name': m.group('last1') or m.group('last2') or ''}
        except:
            ret = {'first_name': value, 'middle_name': '', 'last_name': ''}
        return ret


class TopicPageSingleChoiceField(AutoModelSelect2Field):
    queryset = TopicPage.objects.all_objects()
    search_fields = ['title__icontains']
    empty_values = ['']

    def security_check(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            return True
        else:
            return False


class ContentGroupChoicesField(AutoModelSelect2Field):
    queryset = ContentGroup.objects.all()
    search_fields = ['name__icontains', ]
    empty_values = ['']

    def security_check(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            return True
        else:
            return False
