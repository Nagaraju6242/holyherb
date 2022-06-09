# Generated by Django 3.2.4 on 2021-07-09 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_product_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=50)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('quantity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.quantity_price')),
            ],
        ),
    ]