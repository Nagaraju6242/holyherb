# Generated by Django 3.2.4 on 2021-06-28 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customization', '0018_alter_herobanner_side_heading'),
    ]

    operations = [
        migrations.AddField(
            model_name='herobanner',
            name='order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
