# Generated by Django 3.2.4 on 2023-02-04 23:29

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
            name='User_Matches',
            fields=[
                ('like_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='like_id')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_user', to=settings.AUTH_USER_MODEL, verbose_name='current_user')),
                ('other_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_user', to=settings.AUTH_USER_MODEL, verbose_name='other_user')),
            ],
            options={
                'db_table': 'User_Matches',
            },
        ),
        migrations.CreateModel(
            name='User_Likes',
            fields=[
                ('like_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='like_id')),
                ('message', models.CharField(max_length=300, null=True, verbose_name='message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('userOne', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userOne', to=settings.AUTH_USER_MODEL, verbose_name='userOne')),
                ('userTwo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userTwo', to=settings.AUTH_USER_MODEL, verbose_name='userTwo')),
            ],
            options={
                'db_table': 'User_Likes',
            },
        ),
    ]
