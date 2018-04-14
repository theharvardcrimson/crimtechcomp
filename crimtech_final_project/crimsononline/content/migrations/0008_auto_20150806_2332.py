# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import crimsononline.content.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_content_article_add_parent_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='breakingnews',
            options={'verbose_name': 'breaking news bar', 'verbose_name_plural': 'breaking news bar'},
        ),
        migrations.AlterModelOptions(
            name='contentgroup',
            options={},
        ),
        migrations.AlterModelOptions(
            name='externalcontent',
            options={'verbose_name': 'external content', 'verbose_name_plural': 'external content'},
        ),
        migrations.AlterModelOptions(
            name='flashgraphic',
            options={},
        ),
        migrations.AlterModelOptions(
            name='gallery',
            options={'verbose_name_plural': 'galleries'},
        ),
        migrations.AlterModelOptions(
            name='genericfile',
            options={},
        ),
        migrations.AlterModelOptions(
            name='index',
            options={'verbose_name_plural': 'index'},
        ),
        migrations.AlterModelOptions(
            name='pdf',
            options={'verbose_name': 'PDF'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name_plural': 'videos'},
        ),
        migrations.AddField(
            model_name='contributor',
            name='searchable',
            field=models.BooleanField(default=True, help_text=b"Allow search engines to index this contributor's profile.", db_index=True),
        ),
        migrations.AlterField(
            model_name='externalcontent',
            name='image',
            field=models.ForeignKey(verbose_name=b'associated image', blank=True, to='content.Image', null=True),
        ),
        migrations.AlterField(
            model_name='externalcontent',
            name='redirect_url',
            field=models.CharField(max_length=100, verbose_name=b'redirect URL'),
        ),
        migrations.AlterField(
            model_name='externalcontent',
            name='repr_type',
            field=models.ForeignKey(verbose_name=b'content type', to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='document',
            field=models.FileField(upload_to=crimsononline.content.models.pdf_get_save_path, verbose_name=b'PDF document'),
        ),
        migrations.AlterField(
            model_name='pdf',
            name='thumbnail',
            field=models.ImageField(upload_to=crimsononline.content.models.pdf_thumb_get_save_path, null=True, verbose_name=b'PDF thumbnail', blank=True),
        ),
    ]
