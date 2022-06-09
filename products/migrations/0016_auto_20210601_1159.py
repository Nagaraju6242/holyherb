# Generated by Django 3.1.2 on 2021-06-01 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20210530_1215'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['artistic', 'main_image']},
        ),
        migrations.AlterField(
            model_name='product',
            name='avg_rating',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
