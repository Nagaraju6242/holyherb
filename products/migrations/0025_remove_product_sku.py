# Generated by Django 3.2.4 on 2021-07-27 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_auto_20210709_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
    ]
