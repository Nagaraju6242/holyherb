# Generated by Django 3.2.4 on 2021-07-27 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customization', '0027_alter_font_font_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='font',
            name='color',
            field=models.CharField(default='#080808', max_length=15),
        ),
    ]
