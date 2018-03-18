# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('published_date', models.DateField()),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=150)),
                ('birthday', models.DateField()),
                ('favorite_activities', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('education', models.CharField(max_length=100, choices=[(b'no', b'None'), (b'hs', b'High School'), (b'ug', b'Undergraduate'), (b'ma', b'Masters'), (b'ph', b'PhD')])),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='my_app.Author', null=True),
        ),
    ]
