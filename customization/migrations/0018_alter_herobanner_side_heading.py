# Generated by Django 3.2.4 on 2021-06-28 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customization', '0017_auto_20210628_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='herobanner',
            name='side_heading',
            field=models.TextField(blank=True, null=True),
        ),
    ]
