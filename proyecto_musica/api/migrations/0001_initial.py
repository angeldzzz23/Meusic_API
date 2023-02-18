# Generated by Django 3.2.4 on 2023-02-10 05:41

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Format',
            fields=[
                ('format_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='format_id')),
                ('format_desc', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Format',
            },
        ),
        migrations.CreateModel(
            name='Multimedia_status',
            fields=[
                ('multimedia_status_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='multimedia_status_id')),
                ('multimedia_desc', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Multimedia_status',
            },
        ),
        migrations.CreateModel(
            name='Multimedia_type',
            fields=[
                ('multimedia_type_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='multimedia_type_id')),
                ('multimedia_desc', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'Multimedia_type',
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('video_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='video_id')),
                ('url', models.URLField(null=True)),
                ('title', models.CharField(max_length=50)),
                ('caption', models.CharField(max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('video', models.FileField(upload_to=api.models.get_uplaod_video_name)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
        ),
        migrations.CreateModel(
            name='Multimedia',
            fields=[
                ('multimedia_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='multimedia_id')),
                ('url', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=200)),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.format', verbose_name='format_id')),
                ('multimedia_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.multimedia_status', verbose_name='multimedia_status_id')),
                ('multimedia_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.multimedia_type', verbose_name='multimedia_type_id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'Multimedia',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('image_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='image_id')),
                ('url', models.URLField(null=True)),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to=api.models.get_uplaod_file_name)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'Images',
            },
        ),
    ]
