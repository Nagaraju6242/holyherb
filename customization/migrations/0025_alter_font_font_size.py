# Generated by Django 3.2.4 on 2021-07-26 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customization', '0024_font'),
    ]

    operations = [
        migrations.AlterField(
            model_name='font',
            name='font_size',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]