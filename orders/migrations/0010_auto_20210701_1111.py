# Generated by Django 3.2.4 on 2021-07-01 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20210618_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingmethod',
            name='price',
        ),
        migrations.AddField(
            model_name='shippingmethod',
            name='fixed_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='shippingmethod',
            name='has_fixed_price',
            field=models.BooleanField(default=False, help_text='Either use fixed price or percent discount with min price'),
        ),
        migrations.AddField(
            model_name='shippingmethod',
            name='min_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='shippingmethod',
            name='percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='shippingmethod',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
