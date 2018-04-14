from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    Layout.objects.create(name='Semi-breaking news homepage',
                          template_path='semibreakingnews.html')


def backwards(apps, schema_editor):
    Layout = apps.get_model('placeholders', 'Layout')
    try:
        Layout.objects.get(template_path='semibreakingnews.html').delete()
    except Layout.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('placeholders', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards)
    ]
