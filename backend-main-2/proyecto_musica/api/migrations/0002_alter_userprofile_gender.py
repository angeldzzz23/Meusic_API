# Generated by Django 4.0.5 on 2022-06-28 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='api.gender', verbose_name='gender_id'),
        ),
    ]
