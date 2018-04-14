# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive_photos', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveImage',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Image')),
                ('crimson_owned', models.IntegerField(choices=[(1, b'Yes'), (0, b'No'), (2, b'Unsure')])),
                ('location', models.CharField(default=b'', max_length=100, blank=True)),
                ('subject', models.CharField(default=b'', max_length=100, blank=True)),
                ('show_online', models.BooleanField(default=True)),
                ('sell_online', models.BooleanField(default=False)),
                ('mark_important', models.BooleanField(default=False)),
                ('notes', models.TextField(default=b'', blank=True)),
                ('needs_attention', models.BooleanField(default=False)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('month', models.IntegerField(null=True, blank=True)),
                ('day', models.IntegerField(null=True, blank=True)),
                ('archive_category', models.ForeignKey(to='archive_photos.ArchiveCategory')),
            ],
            options={
            },
            bases=('content.image',),
        ),
        migrations.AddField(
            model_name='archivecategory',
            name='parent',
            field=models.ForeignKey(related_name='children', to='archive_photos.ArchiveCategory', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='archivecategory',
            unique_together=set([('parent', 'name')]),
        ),
    ]
