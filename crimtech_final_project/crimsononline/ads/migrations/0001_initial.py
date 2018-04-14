# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=255)),
                ('network_id', models.CharField(unique=True, max_length=100)),
                ('size', models.CharField(max_length=100)),
                ('display_on', models.IntegerField(default=0, choices=[(0, b'BOTH'), (1, b'Mobile'), (2, b'Desktop')])),
            ],
            options={
                'ordering': ['-size', 'code'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdZone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('ad_units', sortedm2m.fields.SortedManyToManyField(help_text=None, to='ads.AdUnit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
