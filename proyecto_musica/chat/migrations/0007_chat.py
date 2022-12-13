# Generated by Django 3.2.4 on 2022-10-02 00:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0006_inbox_latest_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('message_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='chat_id')),
                ('message', models.CharField(max_length=1000, null=True)),
                ('inbox_user_to_sender', models.CharField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sender_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='sender_id')),
            ],
        ),
    ]
