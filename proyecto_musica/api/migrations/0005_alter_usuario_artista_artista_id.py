# Generated by Django 3.2.4 on 2022-02-27 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_usuario_artista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario_artista',
            name='artista_id',
            field=models.CharField(max_length=100),
        ),
    ]
