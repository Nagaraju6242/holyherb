# Generated by Django 3.1.2 on 2021-06-23 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customization', '0012_homepageingredientindex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepageingredientindex',
            options={'verbose_name': 'Homepage Ingredient Index', 'verbose_name_plural': 'Homepage Ingredient Indexes'},
        ),
        migrations.AlterField(
            model_name='homepageingredientindex',
            name='browse_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]