# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0001_initial'),
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='layout_instance',
            field=models.ForeignKey(to='placeholders.LayoutInstance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='harvardtodayevent',
            name='newsletter',
            field=models.ForeignKey(related_name='events', to='newsletter.HarvardTodayNewsletter'),
            preserve_default=True,
        ),
    ]
