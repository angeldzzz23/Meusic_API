# Generated by Django 3.2.4 on 2023-02-11 03:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_locations'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
    ]
