# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    Layout.objects.create(name='FM Year in Review Gallery',
                          template_path='placeholders/fmyirgallery.html',
                          gallery_template=True)


def backwards(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    try:
        Layout.objects.get(
            template_path='placeholders/fmyirgallery.html').delete()
    except Layout.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0005_layout_gallery_template'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
