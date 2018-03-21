# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
                ('content', models.TextField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birthday', models.DateField()),
                ('favorite_activities', models.TextField(max_length=254)),
                ('email', models.EmailField(max_length=254)),
                ('education', models.CharField(max_length=150, choices=[(b'NONE', b'none'), (b'HIGH_SCHOOL', b'high school'), (b'UNDERGRADUATE', b'undergraduate'), (b'MASTERS', b'masters'), (b'PHD', b'phd')])),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='writer',
            field=models.ForeignKey(to='my_app.Author'),
        ),
    ]
