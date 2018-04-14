# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_auto_20150506_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='parent_topic',
            field=models.ForeignKey(blank=True, to='content.TopicPage', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='contributor_override',
            field=models.TextField(default=b'', help_text=b'Custom HTML to use in place of the auto-generated contributor titles and names. Available only on certain templates.', blank=True),
            preserve_default=True,
        ),
    ]
