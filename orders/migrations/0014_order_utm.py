# Generated by Django 3.2.4 on 2021-10-11 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utm_tracker', '0006_alter_leadsource_user'),
        ('orders', '0013_order_shipment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='utm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utm_tracker.leadsource'),
        ),
    ]
