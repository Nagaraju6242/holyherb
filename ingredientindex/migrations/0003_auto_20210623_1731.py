# Generated by Django 3.1.2 on 2021-06-23 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredientindex', '0002_auto_20210623_1015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',)},
        ),
    ]