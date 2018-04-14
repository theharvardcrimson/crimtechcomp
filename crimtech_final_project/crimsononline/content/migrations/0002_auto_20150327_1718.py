# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0001_initial'),
        ('contenttypes', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicpage',
            name='layout_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='placeholders.LayoutInstance', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='topicpage',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='content.TopicPage', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='section',
            name='layout_instances',
            field=models.ManyToManyField(default=None, to='placeholders.LayoutInstance', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='score',
            name='article',
            field=models.ForeignKey(related_name='sports_scores', to='content.Article'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='score',
            name='sport',
            field=models.ForeignKey(to='content.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='review',
            name='article',
            field=models.ForeignKey(blank=True, to='content.Article', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='packagesectioncontentrelation',
            name='FeaturePackageSection',
            field=models.ForeignKey(related_name='fps', to='content.FeaturePackageSection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='packagesectioncontentrelation',
            name='related_content',
            field=models.ForeignKey(to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mostreadarticles',
            name='article1',
            field=models.ForeignKey(related_name='MostReadArticle1', to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mostreadarticles',
            name='article2',
            field=models.ForeignKey(related_name='MostReadArticle2', to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mostreadarticles',
            name='article3',
            field=models.ForeignKey(related_name='MostReadArticle3', to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mostreadarticles',
            name='article4',
            field=models.ForeignKey(related_name='MostReadArticle4', to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mostreadarticles',
            name='article5',
            field=models.ForeignKey(related_name='MostReadArticle5', to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='marker',
            name='map',
            field=models.ForeignKey(related_name='markers', to='content.Map'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='keyword',
            name='articles',
            field=models.ManyToManyField(related_name='keywords', through='content.ArticleKeywordRelation', to='content.Article'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='index',
            name='layout_instances',
            field=models.ManyToManyField(default=None, to='placeholders.LayoutInstance', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gallerymembership',
            name='content',
            field=models.ForeignKey(related_name='content_set', to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gallerymembership',
            name='gallery',
            field=models.ForeignKey(related_name='gallery_set', to='content.Gallery'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gallery',
            name='contents',
            field=models.ManyToManyField(related_name='galleries_set', through='content.GalleryMembership', to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featurepackagesection',
            name='MainPackage',
            field=models.ForeignKey(related_name='sections', to='content.FeaturePackage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featurepackagesection',
            name='layout',
            field=models.ForeignKey(default=None, blank=True, to='placeholders.Layout', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='featurepackagesection',
            name='related_contents',
            field=models.ManyToManyField(related_name='related_contents', null=True, through='content.PackageSectionContentRelation', to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalcontent',
            name='image',
            field=models.ForeignKey(verbose_name=b'Associated Image', blank=True, to='content.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalcontent',
            name='repr_type',
            field=models.ForeignKey(verbose_name=b'Content Type', to='contenttypes.ContentType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='correction',
            name='article',
            field=models.ForeignKey(to='content.Article'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contenthits',
            name='content',
            field=models.ForeignKey(to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentgroup',
            name='section',
            field=models.ForeignKey(blank=True, to='content.Section', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contentgroup',
            unique_together=set([('type', 'name')]),
        ),
        migrations.AddField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='contributors',
            field=models.ManyToManyField(related_name='content', null=True, to='content.Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='group',
            field=models.ForeignKey(related_name='content', blank=True, to='content.ContentGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='issue',
            field=models.ForeignKey(related_name='content', to='content.Issue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='multimedia_contributors',
            field=models.ManyToManyField(related_name='multimedia_content', null=True, to='content.Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='section',
            field=models.ForeignKey(related_name='content', to='content.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='tags',
            field=models.ManyToManyField(related_name='content', null=True, to='content.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='content',
            unique_together=set([('issue', 'slug')]),
        ),
        migrations.AddField(
            model_name='articlekeywordrelation',
            name='article',
            field=models.ForeignKey(to='content.Article'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlekeywordrelation',
            name='keyword',
            field=models.ForeignKey(to='content.Keyword'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlecontentrelation',
            name='article',
            field=models.ForeignKey(related_name='ar', to='content.Article'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='articlecontentrelation',
            name='related_content',
            field=models.ForeignKey(to='content.Content'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='layout_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='placeholders.LayoutInstance', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='proofer',
            field=models.ForeignKey(related_name='proofed_article_set', blank=True, to='content.Contributor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='rec_articles',
            field=models.ManyToManyField(to='content.Article', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='rel_content',
            field=models.ManyToManyField(related_name='rel_content', null=True, through='content.ArticleContentRelation', to='content.Content', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='sne',
            field=models.ForeignKey(related_name='sned_article_set', blank=True, to='content.Contributor', null=True),
            preserve_default=True,
        ),
    ]
