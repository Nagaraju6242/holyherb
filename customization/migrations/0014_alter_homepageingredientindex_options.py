# Generated by Django 3.2.4 on 2021-06-24 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customization', '0013_auto_20210623_1743'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepageingredientindex',
            options={'ordering': ('name',), 'verbose_name': 'Homepage Ingredient Index', 'verbose_name_plural': 'Homepage Ingredient Indexes'},
        ),
    ]