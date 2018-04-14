# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import crimsononline.newsletter.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HarvardTodayEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.CharField(default=b'', max_length=20)),
                ('description', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('newsletter_type', models.IntegerField(default=0, choices=[(0, b'Daily Newsletter'), (1, b'News Alert'), (2, b'Harvard Today'), (3, b'FM Newsletter'), (4, b'Sports Newsletter'), (5, b'Alumni Newsletter'), (6, b'Special Report'), (7, b'Letterhead Message')])),
                ('created_on', models.DateTimeField()),
                ('send_date', models.DateField(db_index=True, blank=True)),
                ('inline_css', models.BooleanField(default=True)),
                ('ab_split', models.BooleanField(default=True, help_text=b'Enable an A/B split test', verbose_name=b'A/B split')),
                ('subject', models.CharField(max_length=255, blank=True)),
                ('text', models.TextField(default=b'', blank=True)),
            ],
            options={
                'get_latest_by': 'send_date',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HarvardTodayNewsletter',
            fields=[
                ('newsletter_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='newsletter.Newsletter')),
                ('photo_description', models.TextField(default=b'', blank=True)),
                ('weather_description', models.TextField(default=b'', blank=True)),
                ('lunch_description', models.TextField(default=b'', blank=True)),
                ('dinner_description', models.TextField(default=b'', blank=True)),
                ('article_list', models.TextField(default=b'', blank=True)),
            ],
            options={
                'get_latest_by': 'send_date',
            },
            bases=('newsletter.newsletter',),
        ),
        migrations.CreateModel(
            name='NewsletterAd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('pic', models.ImageField(upload_to=crimsononline.newsletter.models.newsletter_image_get_save_path)),
                ('link', models.CharField(max_length=150, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsletterAdFill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('newsletter_id', models.IntegerField(default=0, verbose_name=b'Newsletter Type', choices=[(0, b'Daily Newsletter'), (1, b'News Alert'), (2, b'Harvard Today'), (3, b'FM Newsletter'), (4, b'Sports Newsletter'), (5, b'Alumni Newsletter'), (6, b'Special Report'), (7, b'Letterhead Message')])),
                ('position', models.IntegerField(default=0, choices=[(0, b'Top'), (1, b'Bottom')])),
                ('start_date', models.DateField(db_index=True)),
                ('end_date', models.DateField(db_index=True)),
                ('priority', models.IntegerField(default=1, help_text=b'If multiple ads are scheduled for the same newsletter and date, the one with the higher priority is chosen.')),
                ('ad_copy', models.ForeignKey(to='newsletter.NewsletterAd')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
