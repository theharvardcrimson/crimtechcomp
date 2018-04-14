# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0006_auto_20150505_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placeholder',
            name='autofill_contenttypes',
            field=models.ManyToManyField(to='contenttypes.ContentType', blank=True),
        ),
        migrations.AlterField(
            model_name='placeholder',
            name='autofill_tags',
            field=models.ManyToManyField(related_name='placeholders', to='content.Tag', blank=True),
        ),
    ]
