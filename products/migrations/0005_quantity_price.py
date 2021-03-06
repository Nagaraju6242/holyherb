# Generated by Django 3.1.2 on 2021-04-05 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20210117_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quantity_Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity_type', models.CharField(choices=[('gm', 'GM'), ('ml', 'ML')], default='gm', max_length=100)),
            ],
        ),
    ]
