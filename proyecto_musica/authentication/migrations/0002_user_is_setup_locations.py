# Generated by Django 4.1.4 on 2023-02-26 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_setup',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='user_location_id')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
        ),
    ]
