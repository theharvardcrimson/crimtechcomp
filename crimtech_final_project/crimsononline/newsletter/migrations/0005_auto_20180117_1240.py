# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_auto_20160321_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='newsletter_type',
            field=models.IntegerField(default=0, choices=[(0, b'Daily Newsletter'), (1, b'News Alert'), (2, b'Harvard Today'), (3, b'FM Newsletter'), (4, b'Sports Newsletter'), (5, b'Alumni Newsletter'), (6, b'Special Report'), (7, b'Letterhead Message'), (8, b'Arts Newsletter'), (9, b'Parents Newsletter'), (10, b'Daily Briefing')]),
        ),
        migrations.AlterField(
            model_name='newsletteradfill',
            name='newsletter_id',
            field=models.IntegerField(default=0, verbose_name=b'Newsletter Type', choices=[(0, b'Daily Newsletter'), (1, b'News Alert'), (2, b'Harvard Today'), (3, b'FM Newsletter'), (4, b'Sports Newsletter'), (5, b'Alumni Newsletter'), (6, b'Special Report'), (7, b'Letterhead Message'), (8, b'Arts Newsletter'), (9, b'Parents Newsletter'), (10, b'Daily Briefing')]),
        ),
    ]
