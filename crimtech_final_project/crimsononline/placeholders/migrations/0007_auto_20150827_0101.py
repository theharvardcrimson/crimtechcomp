# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def update_flyby_template_path(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    layout = Layout.objects.get(name='Flyby Section Page')
    layout.template_path = 'flyby/index.html'
    layout.save()

class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0006_auto_20150505_0028'),
    ]

    operations = [
        migrations.RunPython(update_flyby_template_path)
    ]
