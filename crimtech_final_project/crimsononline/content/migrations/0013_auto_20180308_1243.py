# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_auto_20170801_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentgroup',
            name='day_of_week',
            field=models.CharField(blank=True, max_length=70, null=True, help_text=b'Day of week they publish', choices=[(b'm', b'Monday'), (b't', b'Tuesday'), (b'w', b'Wednesday'), (b'th', b'Thursday'), (b'f', b'Friday')]),
        ),
        migrations.AddField(
            model_name='contentgroup',
            name='week',
            field=models.CharField(blank=True, max_length=20, null=True, help_text=b'What week do they publish', choices=[(b'one', b'Week One'), (b'two', b'Week Two'), (b'three', b'Week Three')]),
        ),
        migrations.AlterField(
            model_name='contentgroup',
            name='name',
            field=models.CharField(max_length=70, db_index=True),
        ),
    ]
