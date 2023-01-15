# Generated by Django 4.1.4 on 2023-01-14 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('preferences', '0002_preference_genders_preference_genres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_preference_genders',
            name='preference_gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.genders', verbose_name='preference_gender_id'),
        ),
        migrations.AlterField(
            model_name='user_preference_genres',
            name='preference_genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.genres', verbose_name='preference_genre_id'),
        ),
        migrations.AlterField(
            model_name='user_preference_skills',
            name='preference_skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.skills', verbose_name='preference_skill_id'),
        ),
        migrations.AlterField(
            model_name='user_preferences_age',
            name='preference_age_id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, unique=True, verbose_name='preference_age_id'),
        ),
        migrations.DeleteModel(
            name='Preference_Genders',
        ),
        migrations.DeleteModel(
            name='Preference_Genres',
        ),
        migrations.DeleteModel(
            name='Preference_Skills',
        ),
    ]
