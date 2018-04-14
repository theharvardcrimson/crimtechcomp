"""
Forms, widgets, fields.
However, put forms specifically for Admin in admin.py, not here
"""

import logging
from datetime import date, datetime, timedelta
from re import compile
from time import strptime

from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from crimsononline.content.models import Content, Issue, Tag

logger = logging.getLogger(__name__)


class TagSelectWidget(forms.SelectMultiple):
    """A SelectMultiple with a JavaScript filter interface.

    This is designed only to be used in the admin interface.  Will probably
    not work elsewhere without many 1337 haxx / patches.  Note that the
    resulting JavaScript assumes that the jsi18n
    catalog has been loaded in the page.
    """
    class Media:
        js = ('admin/js/core.js',
              'admin/js/SelectBox.js',
              'scripts/admin/SelectTag.js',)

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=(),
                 tag_qs=None):
        if tag_qs is None:
            tag_qs = Tag.objects.all()
        categories = Tag.CATEGORY_CHOICES
        tag_dict = {}
        for short, verbose in categories:
            tag_dict[verbose] = tag_qs.filter(category=short)
        self.verbose_name = verbose_name
        self.is_stacked = is_stacked
        super(TagSelectWidget, self).__init__(attrs, choices)
        self.tags = tag_dict

    def render(self, name, value, attrs=None, choices=()):
        owidg = super(TagSelectWidget, self).render(
            name, value, attrs, choices)
        vname = self.verbose_name.replace('"', '\\"')
        is_stacked = int(self.is_stacked)
        adm_media_prefix = settings.STATIC_URL + 'admin/'
        categories = self.tags
        return mark_safe(render_to_string('forms/select_tag_array.html',
                                          locals()))


class MapBuilderWidget(forms.widgets.HiddenInput):

    class Media:
        js = ('scripts/admin/framework/jquery-ui.packed.js',)

    def render(self, name, value, attrs=None):
        googleapikey = settings.GOOGLE_API_KEY
        return render_to_string('forms/map_builder_widget.html', locals())


class MapBuilderField(forms.CharField):
    """
    A field that allows you to add a map via a map builder.

    Always uses the MapBuilderWidget.
    """

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = MapBuilderWidget()
        return super(MapBuilderField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value:
            if self.required:
                raise forms.ValidationError("This can't be left blank")
            return
        return


class IssuePickerWidget(forms.widgets.HiddenInput):
    """
    Widget that uses a calendar picker and ajax to pick issues.
    """

    class Media:
        js = ('scripts/admin/framework/jquery-ui.packed.js',
              'scripts/admin/IssuePickerWidget.js',)
        css = {
            'all': ('css/admin/framework/jquery.ui.css',
                    'css/admin/IssuePickerWidget.css',)
        }

    def __init__(self, *args, **kwargs):
        self.editable = True
        super(IssuePickerWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        meta_select = 'daily'
        if value:
            # this assumes that there are no errors (the field gets
            # cleaned correctly) if there's an error that needs to be
            # corrected on the form, then the next line won't work,
            # since value will be a date string
            try:
                issue = Issue.objects.get(pk=int(value))
                issue_date = issue.issue_date
                if issue.special_issue_name:
                    meta_select = 'special'
            except ValueError:
                dt = strptime(value, r'%m/%d/%Y')
                issue_date = date(dt[0], dt[1], dt[2])
        else:
            # default value is the next issue
            issue_date = datetime.now()
            if issue_date.hour > 11:
                issue_date = issue_date.date() + timedelta(days=1)
            else:
                issue_date = issue_date.date()
            value = issue_date.strftime(r'%m/%d/%Y')
        year = datetime.now().year
        special_choices = render_to_string(
            'ajax/special_issues_fragment.html',
            {'issues': Issue.objects.special.filter(issue_date__year=year),
             'blank': '----', 'choice': value}
        )
        is_editable = self.editable
        hidden = super(IssuePickerWidget, self).render(name, value, attrs)
        static_url = settings.STATIC_URL
        return render_to_string('forms/issue_picker_widget.html', locals())


class IssuePickerField(forms.CharField):
    """
    A field that allows you to pick an issue via a date picker.

    Always uses the IssuePickerWidget.
    """

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = IssuePickerWidget()
        return super(IssuePickerField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value:
            if self.required:
                raise forms.ValidationError("This can't be left blank")
            return
        # if the value is in dd/mm/yyyy format, look for / create an issue

        DATE_FMT = compile(r'\d{2}/\d{2}/\d{4}')
        if DATE_FMT.match(value):
            dt = strptime(value, r'%m/%d/%Y')
            dt = date(dt[0], dt[1], dt[2])
            try:
                issue = Issue.objects.daily.filter(issue_date=dt)[0]
            except ObjectDoesNotExist:
                issue = Issue(issue_date=dt)
                issue.save()
            except:
                issue = Issue(issue_date=dt)
                issue.save()

            return issue
        # otherwise, grab the (special) issue from db
        else:
            try:
                return Issue.objects.get(pk=int(value))
            except:  # the frontend should ensure these errors never happen
                raise forms.ValidationError('Something terrible happened!')


class RelatedContentWidget(forms.widgets.HiddenInput):
    class Media:
        js = ('scripts/admin/framework/jquery-ui.packed.js',
              'scripts/admin/RelatedContentWidget.js')
        css = {
            'all': ('css/admin/framework/jquery.ui.css',
                    'css/admin/RelatedContent.css')
        }

    def __init__(self, *args, **kwargs):
        self.rel_types = kwargs.pop('rel_types', None)
        self.c_types = []
        self.max = kwargs.pop('limit', None)

        return super(RelatedContentWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        # set up content types
        self.c_types = []
        for t in self.rel_types:
            t_name = t._meta.object_name
            t_url = '../../../%s/%s/' % (t._meta.app_label, t_name.lower())
            t_id = ContentType.objects.get_for_model(t).pk
            self.c_types.append({'url': t_url, 'name': t_name, 'id': t_id})

        if value:
            # deal with old stuff
            if isinstance(value, basestring):
                value = [int(v) for v in value.split(';') if v]
                # grab all related content objects AND PRESERVE ORDER !!
                objs = []
                for v in value:
                    try:
                        objs.append({
                            'related_content': Content.objects.admin_objects()
                                                              .get(pk=v),
                            'shortcoded': False})
                    except:
                        pass

                # construct related content identifiers
                value = ['%d' % (o['related_content'].pk)
                         for o in objs if o]
                value = ';'.join(value) + ';'
            else:
                # assume we have an array of ACR's
                objs = []
                for v in value:
                    try:
                        objs.append(v)
                    except:
                        pass
                value = ['%d' % (o.related_content.pk)
                         for o in objs if o]
                value = ';'.join(value) + ';'
        else:
            # make sure value isn't '', [], or some other fail
            value = None

        hidden = super(RelatedContentWidget, self).render(name, value, attrs)
        # account for closeouts before midnight
        today = datetime.now() + timedelta(days=1)
        yesterday = datetime.now() + timedelta(days=-2)
        types = self.c_types
        if self.max:
            limit = self.max
        return render_to_string('forms/related_content_widget.html', locals())


class RelatedContentField(forms.CharField):
    """The interface for adding / editing related content."""

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = RelatedContentWidget(
            rel_types=kwargs.pop('rel_types', []),
            limit=kwargs.pop('limit', None)
        )
        return super(RelatedContentField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """Turns value into a list of Content objects

        value is received as a ; delimited set of primary keys
        """

        if not value:
            return []
        ids = [int(id) for id in value.split(';') if id]
        q = reduce(lambda x, y: x | y, [Q(pk=p) for p in ids])
        objs = list(Content.objects.admin_objects().filter(q))
        # retrieving Content objs MUST preserve their order!!!
        objs = dict([(obj.pk, obj) for obj in objs])

        return [objs[pk] for pk in ids]
