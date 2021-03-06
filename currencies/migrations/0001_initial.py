# Generated by Django 3.1.7 on 2021-03-21 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='currency code', max_length=10, unique=True)),
                ('value', models.FloatField(default=1, help_text='current value compared to Eur')),
                ('last_updated', models.DateField(auto_now=True)),
            ],
        ),
    ]
