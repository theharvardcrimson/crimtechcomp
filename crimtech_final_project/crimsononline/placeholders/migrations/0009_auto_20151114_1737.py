# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    Layout.objects.create(name='Spotlight Light Topic Page',
                          template_path='models/topicpage/spotlight-light/landing.html',
                          gallery_template=True)


def backwards(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    try:
        Layout.objects.get(
            template_path='models/topicpage/spotlight-light/landing.html').delete()
    except Layout.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0008_merge'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
