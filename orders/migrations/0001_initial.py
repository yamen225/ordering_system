# Generated by Django 3.1.7 on 2021-03-21 08:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(help_text='order amount in buyer currency - must be gt 0 and equal to product price', validators=[django.core.validators.MinValueValidator(1)])),
                ('buyer', models.ForeignKey(help_text='buyer of order from user model - must not be admin', on_delete=django.db.models.deletion.DO_NOTHING, related_name='bought', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(help_text='Product id being purchased', on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='products.product')),
            ],
        ),
    ]