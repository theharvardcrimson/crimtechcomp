# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0004_auto_20150504_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='layout',
            name='gallery_template',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
