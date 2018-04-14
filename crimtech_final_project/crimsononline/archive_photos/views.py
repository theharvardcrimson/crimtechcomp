from django import forms
from django.contrib import admin
from django.shortcuts import render

from .models import ArchiveImage


class ArchiveForm(forms.ModelForm):
    class Media:
        css = {
            'all': ('admin/css/widgets.css',),
        }
        js = (
            'admin/js/core.js',
            'admin/js/jquery.min.js',
            'admin/js/jquery.init.js',
            'admin/js/SelectBox.js',
            'admin/js/addevent.js',
            '/admin/jsi18n/',
        )

    class Meta:
        model = ArchiveImage
        fields = ('title', 'subtitle', 'contributors', 'pic', 'crimson_owned',
                  'description', 'location', 'show_online', 'sell_online',
                  'archive_category', 'tags', 'slug', 'notes')
        widgets = {
            'tags': admin.widgets.FilteredSelectMultiple(
                'Tags', False, attrs={'rows': '2'}),
            'contributors': admin.widgets.FilteredSelectMultiple(
                'Contributors', False, attrs={'rows': '2'}),
        }


def upload_view(request):
    data = {'valid': False}

    if request.method == 'POST':
        data['form'] = ArchiveForm(request.POST)
        if data['form'].is_valid():
            # process form
            data['valid'] = True
            data['form'] = ArchiveForm()
    else:
        data['form'] = ArchiveForm()

    return render(request, 'archive_uploader.html', data)
