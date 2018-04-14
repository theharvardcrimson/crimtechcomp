# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0003_auto_20150826_0229'),
    ]

    operations = [
        migrations.CreateModel(
            name='HarvardTodaySponsoredEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.CharField(default=b'', max_length=20)),
                ('description', models.TextField(default=b'')),
            ],
        ),
        migrations.AddField(
            model_name='harvardtodaynewsletter',
            name='others_list',
            field=models.TextField(default=b'', blank=True),
        ),
        migrations.AddField(
            model_name='harvardtodaysponsoredevent',
            name='newsletter',
            field=models.ForeignKey(related_name='sponsored_events', to='newsletter.HarvardTodayNewsletter'),
        ),
    ]
