# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_fm_sections(apps, schema_editor):
    Section = apps.get_model('content', 'Section')
    for name in ['FM: Levity', 'FM: Around Town', 'FM: Introspection',
                 'FM: Conversations', 'FM: Retrospection']:
        section = Section(name=name, can_have_articles=False)
        section.save()

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_auto_20151123_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='can_have_articles',
            field=models.BooleanField(default=True, help_text=b'Whether articles can belong to this section'),
        ),
        migrations.RunPython(add_fm_sections)
    ]
