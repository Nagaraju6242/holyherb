# Generated by Django 3.1.2 on 2021-05-30 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20210530_1215'),
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_quantity', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
            ],
        ),
    ]
