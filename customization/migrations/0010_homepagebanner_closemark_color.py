# Generated by Django 3.1.2 on 2021-06-18 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customization', '0009_auto_20210611_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagebanner',
            name='closemark_color',
            field=models.CharField(default='#000', max_length=20),
        ),
    ]
