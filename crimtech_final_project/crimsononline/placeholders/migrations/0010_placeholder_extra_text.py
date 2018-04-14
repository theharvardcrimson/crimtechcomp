# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0009_auto_20151114_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeholder',
            name='extra_text',
            field=models.TextField(blank=True),
        ),
    ]
