# Generated by Django 3.1.2 on 2021-04-05 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='flavour',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]