# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20150406_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='contributor_override',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
