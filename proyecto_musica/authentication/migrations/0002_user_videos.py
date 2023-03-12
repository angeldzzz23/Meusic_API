# Generated by Django 3.2.4 on 2023-03-10 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Videos',
            fields=[
                ('vid_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='vimeo_id')),
                ('video_id', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'User_Videos',
            },
        ),
    ]
