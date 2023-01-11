from django.db import models
from authentication.models import User, Genres, Genders, Skills

class User_Preferences_Genders(models.Model):
    preference_gender_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='user_gender_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    genders = models.ForeignKey(
        Genders,
        on_delete=models.CASCADE,
        verbose_name='gender_id'
    )

    class Meta:
        db_table = 'User_Preferences_Genders'


class User_Preferences_Skills(models.Model):
    preference_skill_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='user_skill_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    skills = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='skill_id'
    )

    class Meta:
        db_table = 'User_Preferences_Skills'


class User_Preferences_Genres(models.Model):
    preference_genre_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='user_genre_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    genres = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='genre_id'
    )

    class Meta:
        db_table = 'User_Preferences_Genres'


class User_Preferences_Age(models.Model):
    preference_age_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='user_age_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    age_low = models.IntegerField(verbose_name='age_low')
    age_high = models.IntegerField(verbose_name='age_high')

    class Meta:
        db_table = 'User_Preferences_Age'


class User_Preferences_Distance(models.Model):
    preference_distance_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='user_distance_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    distance_low = models.IntegerField(verbose_name='distance_low')
    distance_high = models.IntegerField(verbose_name='distance_high')

    class Meta:
        db_table = 'User_Preferences_Distance'


class User_Preferences_Globally(models.Model):
    preference_globally_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='user_globally_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    isGlobal = models.BooleanField(verbose_name='is_global')

    class Meta:
        db_table = 'User_Preferences_Globally'
