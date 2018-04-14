# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_section_can_have_articles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='byline_type',
            field=models.CharField(blank=True, max_length=70, null=True, help_text=b'This will automatically be pluralized if there are multiple contributors.', choices=[(b'cstaff', b'Crimson Staff Writer'), (b'contrib', b'Contributing Writer'), (b'opinion', b'Crimson Opinion Writer'), (b'opinion_contrib', b'Contributing Opinion Writer')]),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='_title',
            field=models.CharField(blank=True, max_length=70, null=True, verbose_name=b'title', choices=[(b'cstaff', b'Crimson staff writer'), (b'contrib', b'Contributing writer'), (b'photog', b'Photographer'), (b'design', b'Designer'), (b'editor', b'Editor'), (b'opinion', b'Crimson opinion writer'), (b'opinion_contrib', b'Contributing opinion writer')]),
        ),
    ]
