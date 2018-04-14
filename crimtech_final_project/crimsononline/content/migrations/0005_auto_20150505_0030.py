# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0006_auto_20150505_0028'),
        ('content', '0004_content_contributor_override'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='layout_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='placeholders.LayoutInstance', null=True),
            preserve_default=True,
        )
    ]
