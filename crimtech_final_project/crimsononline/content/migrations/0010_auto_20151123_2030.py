# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='proofer',
        ),
        migrations.RemoveField(
            model_name='article',
            name='sne',
        ),
        migrations.RemoveField(
            model_name='article',
            name='web_only',
        ),
    ]
