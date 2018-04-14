# TODO: this should be forms.py. Changed before merging

import logging

from django import forms

from crimsononline.content.admin import ContentModelForm
from crimsononline.content.models import Contributor, Tag
from crimsononline.imageuploader.models import BulkImage

logger = logging.getLogger(__name__)


class BulkImageForm(ContentModelForm):
    # django_select2's implementation plus our enormous list of
    # contributors causes browsers to hang when inserting additional select
    # boxes because of all the data being replicated. We will have one
    # Javascript list that all boxes refer to instead.
    contributors = forms.CharField(widget=forms.HiddenInput())
    multimedia_contributors = forms.CharField(widget=forms.HiddenInput(),
                                              required=False)

    # Tags widget will not work with multiple tag selectors. This will be
    # replaced with a select2 widget
    tags = forms.CharField(widget=forms.HiddenInput())

    # Used to match the metadata with the file in the temporary uploads bucket
    filename = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = BulkImage
        # Note: some of these will be hidden. Present by default are:
        # 'title', 'subtitle', 'description', 'contributors', 'tags', 'slug'
        fields = ('publishable', 'sell_online', 'pending_review', 'title',
                  'subtitle', 'description', 'contributors',
                  # 'multimedia_contributors', 'contributor_override',
                  'tags',
                  'issue', 'slug', 'section', 'priority', 'group',
                  'pub_status', 'searchable', 'show_ads')

    def __init__(self, *args, **kwargs):
        super(BulkImageForm, self).__init__(*args, **kwargs)
        # Add a 'placeholder' attribute to all fields
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['class'] = field_name
            field.widget.attrs['placeholder'] = \
                field.label or field_name.capitalize()

    def clean(self):
        """
        Really hacky. Never do this. This is only necessary since
        django_select2 does not play nicely with dynamically added forms
        """

        cleaned_data = super(BulkImageForm, self).clean()
        select2_fields = (
            ('contributors', Contributor),
            ('multimedia_contributors', Contributor),
            ('tags', Tag))
        for field_name, cls in select2_fields:
            values = cleaned_data.get(field_name)
            if not values:
                continue
            values = values.split(',')
            values = cls.objects.filter(id__in=values)
            cleaned_data[field_name] = values
        return cleaned_data
