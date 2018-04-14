# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('description', models.CharField(max_length=300, blank=True)),
                ('template_path', models.CharField(unique=True, max_length=100)),
                ('pic', models.ImageField(null=True, upload_to=b'layouts', blank=True)),
                ('article_template', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LayoutInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('custom_html', models.TextField(blank=True)),
                ('parent', models.ForeignKey(to='placeholders.Layout')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Placeholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=50, blank=True)),
                ('title_link', models.CharField(max_length=100, blank=True)),
                ('min_items', models.IntegerField(null=True, blank=True)),
                ('position', models.IntegerField(null=True, blank=True)),
                ('autofill_prioritize', models.BooleanField(default=False)),
                ('autofill_number', models.IntegerField(default=0)),
                ('require_media', models.BooleanField(default=False)),
                ('autofill_contenttypes', models.ManyToManyField(to='contenttypes.ContentType', null=True, blank=True)),
                ('autofill_section', models.ForeignKey(related_name='placeholders', blank=True, to='content.Section', null=True)),
                ('autofill_tags', models.ManyToManyField(related_name='placeholders', null=True, to='content.Tag', blank=True)),
                ('layout', models.ForeignKey(related_name='placeholders', to='placeholders.LayoutInstance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaceholderContentRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('position', models.IntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('placeholder', models.ForeignKey(related_name='content_relations', to='placeholders.Placeholder')),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='placeholdercontentrelation',
            unique_together=set([('placeholder', 'position')]),
        ),
        migrations.AlterUniqueTogether(
            name='placeholder',
            unique_together=set([('layout', 'name'), ('layout', 'position')]),
        ),
    ]
