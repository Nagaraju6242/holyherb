# Generated by Django 3.2.4 on 2021-10-11 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('utm_tracker', '0005_auto_20210809_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadsource',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lead_sources', to=settings.AUTH_USER_MODEL),
        ),
    ]
