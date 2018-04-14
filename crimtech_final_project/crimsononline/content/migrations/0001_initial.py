# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import crimsononline.content.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleContentRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('shortcoded', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleKeywordRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BreakingNews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Breaking News', max_length=50, blank=True)),
                ('text', models.CharField(max_length=250, blank=True)),
                ('link', models.URLField(max_length=250, blank=True)),
                ('updated', models.TimeField(null=True, blank=True)),
                ('enabled', models.BooleanField(default=False)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Alert Bar',
                'verbose_name_plural': 'Alert Bar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=200)),
                ('subtitle', models.CharField(default=b'', max_length=255, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
                ('slug', models.SlugField(help_text=b'\n        The text that will be displayed in the URL of this article.\n        Can only contain letters, numbers, and dashes (-).\n        ', max_length=70)),
                ('priority', models.IntegerField(default=3, db_index=True, choices=[(1, b'1 | one off articles'), (2, b'2 |'), (4, b'3 | a normal article'), (5, b'4 |'), (6, b'5 |'), (7, b'6 | kind of a big deal'), (9, b'7 | lasts ~2 days'), (13, b'8 |'), (17, b'9 | ~ 4 days'), (21, b"10 | OMG, It's Faust!")])),
                ('pub_status', models.IntegerField(default=0, db_index=True, choices=[(0, b'Draft'), (1, b'Published'), (-1, b'Deleted')])),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_on', models.DateTimeField(db_index=True)),
                ('old_pk', models.IntegerField(help_text=b'primary key from the old website.', null=True, db_index=True)),
                ('searchable', models.BooleanField(default=True, help_text=b'Allow search engines to index this content', db_index=True)),
                ('paginate', models.BooleanField(default=True, help_text=b'Allow article to be paginated')),
                ('show_ads', models.BooleanField(default=True)),
            ],
            options={
                'get_latest_by': 'created_on',
                'permissions': (('content.can_publish', 'Can publish content'), ('content.can_unpublish', 'Can unpublish content'), ('content.can_delete_published', 'Can delete published content'), ('make_unsearchable_content', 'Can hide content from search engines'), ('can_hide_ads', 'Can prevent ads from displaying on content')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('byline_type', models.CharField(blank=True, max_length=70, null=True, help_text=b'This will automatically be pluralized if there are multiple contributors.', choices=[(b'cstaff', b'Crimson Staff Writer'), (b'contrib', b'Contributing Writer')])),
                ('text', models.TextField()),
                ('page', models.CharField(help_text=b'Page in the print edition.', max_length=10, null=True, blank=True)),
                ('web_only', models.BooleanField(default=False)),
                ('tagline', models.BooleanField(default=False, help_text=b'Auto-generate the tagline.')),
            ],
            options={
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='ContentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(db_index=True, max_length=25, choices=[(b'column', b'Column'), (b'series', b'Series'), (b'blog', b'Blog')])),
                ('name', models.CharField(max_length=35, db_index=True)),
                ('subname', models.CharField(max_length=40, null=True, blank=True)),
                ('blurb', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(help_text=b'Thumbnail', null=True, upload_to=crimsononline.content.models.get_img_path, blank=True)),
                ('active', models.BooleanField(default=True, help_text=b'ContentGroups that could still have content posted to them are active.  Active blogs and columnists show up on section pages.', db_index=True)),
            ],
            options={
                'verbose_name_plural': 'Content Groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentHits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True, db_index=True)),
                ('hits', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=70, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('middle_name', models.CharField(max_length=70, null=True, blank=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, help_text=b'This should be true for anyone who could possibly still write for The Crimson, including guest writers.', db_index=True)),
                ('bio_text', models.CharField(help_text=b'Short biographical blurb about yourself, less than 500 characters.', max_length=500, null=True, blank=True)),
                ('image', models.ImageField(help_text=b'This should be a profile picture.', null=True, upload_to=crimsononline.content.models.contrib_pic_path, blank=True)),
                ('twitter', models.CharField(help_text=b'Your username without the @ sign.', max_length=70, null=True, blank=True)),
                ('email', models.CharField(help_text=b'In the form of email@thecrimson.com.', max_length=70, null=True, blank=True)),
                ('gender', models.CharField(default=b'other', choices=[(b'f', b'Female'), (b'm', b'Male'), (b'other', b'Other')], max_length=70, blank=True, help_text=b'Important for generating article taglines correctly.', null=True)),
                ('_title', models.CharField(blank=True, max_length=70, null=True, verbose_name=b'title', choices=[(b'cstaff', b'Crimson staff writer'), (b'contrib', b'Contributing writer'), (b'photog', b'Photographer'), (b'design', b'Designer'), (b'editor', b'Editor')])),
            ],
            options={
                'ordering': ('last_name',),
                'permissions': (('contributor.can_merge', 'Can merge contributor profiles'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('dt', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalContent',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('redirect_url', models.CharField(max_length=100, verbose_name=b'Redirect URL')),
            ],
            options={
                'verbose_name': 'External Content',
                'verbose_name_plural': 'External Content',
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='FeaturePackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('pub_status', models.IntegerField(default=0, db_index=True, choices=[(0, b'Draft'), (1, b'Published'), (-1, b'Deleted')])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('feature', models.BooleanField(default=False)),
                ('slug', models.CharField(max_length=250, blank=True)),
                ('banner', models.ImageField(null=True, upload_to=crimsononline.content.models.package_pic_path, blank=True)),
            ],
            options={
                'permissions': (('content.can_publish', 'Can publish content'), ('content.can_unpublish', 'Can unpublish content'), ('content.can_delete_published', 'Can delete published content')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeaturePackageSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('icon', models.ImageField(null=True, upload_to=crimsononline.content.models.package_pic_path, blank=True)),
                ('pub_status', models.IntegerField(default=0, db_index=True, choices=[(0, b'Draft'), (1, b'Published'), (-1, b'Deleted')])),
                ('slug', models.CharField(max_length=250, blank=True)),
            ],
            options={
                'permissions': (('content.can_publish', 'Can publish content'), ('content.can_unpublish', 'Can unpublish content'), ('content.can_delete_published', 'Can delete published content')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FlashGraphic',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('graphic', models.FileField(upload_to=crimsononline.content.models.misc_get_save_path)),
                ('pic', models.ImageField(upload_to=crimsononline.content.models.misc_get_save_path)),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name_plural': 'Flash Graphics',
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
            ],
            options={
                'verbose_name_plural': 'Galleries',
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='GalleryMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GenericFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gen_file', models.FileField(upload_to=crimsononline.content.models.genericfile_get_save_path, verbose_name=b'File')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name_plural': 'Generic Files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('pic', models.ImageField(height_field=b'height', width_field=b'width', upload_to=crimsononline.content.models.image_get_save_path)),
                ('crop_x', models.IntegerField(null=True)),
                ('crop_y', models.IntegerField(null=True)),
                ('crop_side', models.IntegerField(null=True)),
                ('width', models.PositiveIntegerField(null=True)),
                ('height', models.PositiveIntegerField(null=True)),
                ('is_archiveimage', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Index',
                'verbose_name_plural': 'Index',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('special_issue_name', models.CharField(help_text=b'Leave this blank for daily issues!!!', max_length=100, null=True, db_index=True, blank=True)),
                ('web_publish_date', models.DateTimeField(help_text=b'When this issue goes live (on the web).', null=True)),
                ('issue_date', models.DateField(help_text=b'Corresponds with date of print edition.', db_index=True)),
                ('fm_name', models.CharField(help_text=b'The name of the FM issue published on this issue date', max_length=100, null=True, verbose_name=b'FM name', blank=True)),
                ('arts_name', models.CharField(help_text=b'The name of the Arts issue published on this issue date', max_length=100, null=True, blank=True)),
                ('comments', models.TextField(help_text=b'Notes about this issue.', null=True, blank=True)),
            ],
            options={
                'ordering': ['-issue_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(unique=True, max_length=150, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('zoom_level', models.PositiveSmallIntegerField(default=15)),
                ('center_lat', models.FloatField(default=42.373002)),
                ('center_lng', models.FloatField(default=-71.11905)),
                ('display_mode', models.CharField(default=b'Map', max_length=50)),
                ('width', models.IntegerField(default=b'300')),
                ('height', models.IntegerField(default=b'300')),
            ],
            options={
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.FloatField(db_index=True)),
                ('lng', models.FloatField(db_index=True)),
                ('color', models.CharField(default=b'red', max_length=255, choices=[(b'yellow', b'Yellow'), (b'blue', b'Blue'), (b'green', b'Green'), (b'ltblue', b'Light blue'), (b'orange', b'Orange'), (b'pink', b'Pink'), (b'purple', b'Purple'), (b'red', b'Red')])),
                ('popup_text', models.CharField(help_text=b'text that appears when the user clicks the marker', max_length=1000, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MostReadArticles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackageSectionContentRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('isFeatured', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PDF',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('document', models.FileField(upload_to=crimsononline.content.models.pdf_get_save_path, verbose_name=b'PDF Document')),
                ('thumbnail', models.ImageField(upload_to=crimsononline.content.models.pdf_thumb_get_save_path, null=True, verbose_name=b'PDF Thumbnail', blank=True)),
            ],
            options={
                'verbose_name': 'PDF',
                'verbose_name_plural': 'PDFs',
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=10, choices=[(b'movie', b'Movie'), (b'music', b'Music'), (b'book', b'Book')])),
                ('name', models.CharField(max_length=100)),
                ('rating', models.IntegerField(db_index=True, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opponent', models.CharField(max_length=50, null=True, blank=True)),
                ('our_score', models.CharField(max_length=20, null=True, blank=True)),
                ('their_score', models.CharField(max_length=20, null=True, blank=True)),
                ('home_game', models.BooleanField(default=True)),
                ('text', models.CharField(max_length=50, null=True, blank=True)),
                ('event_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, db_index=True)),
                ('audiodizer_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('csv_file', models.FileField(upload_to=crimsononline.content.models.misc_get_save_path)),
                ('json_file', models.FileField(upload_to=crimsononline.content.models.misc_get_save_path)),
            ],
            options={
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(help_text=b'Tags can contain letters and spaces', unique=True, max_length=40, db_index=True)),
                ('category', models.CharField(blank=True, max_length=25, db_index=True, choices=[(b'sports', b'Sports'), (b'college', b'College'), (b'faculty', b'Faculty'), (b'university', b'University'), (b'city', b'City'), (b'stugroups', b'Student Groups'), (b'houses', b'Houses'), (b'depts', b'Departments'), (b'', b'Uncategorized')])),
                ('is_vague', models.BooleanField(default=False, help_text=b'Vague tags are those that are too broad or so widely                 used that they should not be taken into account when                 recommended articles are generated.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TopicPage',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('pos', models.IntegerField(default=0, verbose_name=b'Position (only useful if there is a parent topic)', blank=True)),
                ('image', models.ForeignKey(verbose_name=b'Associated Image', blank=True, to='content.Image', null=True)),
            ],
            options={
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('key', models.CharField(help_text=b'youtube.com/watch?v=(XXXXXX)&... part of the YouTube URL. NOTE: THIS IS NOT THE ENTIRE YOUTUBE URL.', max_length=100, db_index=True)),
                ('pic', models.ImageField(null=True, upload_to=crimsononline.content.models.youtube_get_save_path)),
            ],
            options={
                'verbose_name_plural': 'Videos',
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('content_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='content.Content')),
                ('html', models.TextField()),
                ('javascript', models.TextField()),
                ('is_highcharts', models.BooleanField(default=False)),
                ('is_d3', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=('content.content',),
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=150, db_index=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('word_frequency', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
