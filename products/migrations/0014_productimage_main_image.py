# Generated by Django 3.1.2 on 2021-05-29 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20210527_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='main_image',
            field=models.BooleanField(default=False),
        ),
    ]