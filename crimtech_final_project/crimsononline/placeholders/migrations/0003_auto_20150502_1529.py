# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    Layout.objects.create(name='FM Year in Review',
                          template_path='fmyearinreview.html')

def backwards(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    try:
        Layout.objects.get(template_path='fmyearinreview.html').delete()
    except Layout.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0002_auto_20150415_1345'),
    ]

    operations = [
      migrations.RunPython(forwards, backwards),
    ]
