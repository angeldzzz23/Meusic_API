# Generated by Django 3.2.4 on 2023-02-15 03:10

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20230214_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locations',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326),
        ),
    ]
