# Generated by Django 3.1.2 on 2021-06-09 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20210601_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='handpicked',
            field=models.BooleanField(default=False),
        ),
    ]
