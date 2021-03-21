# Generated by Django 3.1.7 on 2021-03-21 08:16

from django.db import migrations


def populate_currencies(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Currency = apps.get_model('currencies', 'Currency')
    Currency.objects.create(code='EUR', value=1)


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_currencies),
    ]
