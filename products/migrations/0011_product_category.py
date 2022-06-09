# Generated by Django 3.1.2 on 2021-04-18 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210407_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('haircare', 'Hair Care'), ('facecare', 'Face Care'), ('bodycare', 'Body Care'), ('feetcare', 'Feet Care')], default='haircare', max_length=100, null=True),
        ),
    ]