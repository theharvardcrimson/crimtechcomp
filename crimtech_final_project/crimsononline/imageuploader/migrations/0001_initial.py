# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulkImage',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Image')),
                ('publishable', models.BooleanField(default=False)),
                ('sell_online', models.BooleanField(default=True)),
                ('pending_review', models.BooleanField(default=True)),
            ],
            bases=('content.image',),
        ),
    ]
