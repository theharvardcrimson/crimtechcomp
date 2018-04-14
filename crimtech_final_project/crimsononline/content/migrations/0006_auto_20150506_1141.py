# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import crimsononline.content.models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20150505_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='pic',
            field=models.ImageField(upload_to=crimsononline.content.models.misc_get_save_path, blank=True),
            preserve_default=True,
        ),
    ]
