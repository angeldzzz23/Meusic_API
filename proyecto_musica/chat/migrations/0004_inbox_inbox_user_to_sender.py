# Generated by Django 3.2.4 on 2022-10-01 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20221001_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='inbox_user_to_sender',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
