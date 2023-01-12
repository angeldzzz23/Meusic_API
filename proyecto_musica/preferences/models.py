from django.db import models
from authentication.models import User

class Preference_Genders(models.Model):
    preference_gender_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='preference_gender_id',
    )
    preference_gender_name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.preference_gender_id
    class Meta:
        db_table = 'Preference_Genders'


class User_Preference_Genders(models.Model):
    preference_user_gender_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='preference_user_gender_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    preference_gender = models.ForeignKey(
        Preference_Genders,
        on_delete=models.CASCADE,
        verbose_name='preference_gender_id'
    )

    class Meta:
        db_table = 'Preference_User_Genders'


class Preference_Skills(models.Model):
    preference_skill_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='preference_skill_id',
    )
    preference_skill_name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.preference_skill_id
    class Meta:
        db_table = 'Preference_Skills'


class User_Preference_Skills(models.Model):
    user_skill_id = models.BigAutoField(
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
    preference_skill = models.ForeignKey(
        Preference_Skills,
        on_delete=models.CASCADE,
        verbose_name='preference_skill_id'
    )

    class Meta:
        db_table = 'User_Preference_Skills'


class Preference_Genres(models.Model):
    preference_genre_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='preference_genre_id',
    )
    preference_genre_name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.preference_genre_id
    class Meta:
        db_table = 'Preference_Genres'


class User_Preference_Genres(models.Model):
    user_preference_genre_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='user_preference_genre_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    preference_genre = models.ForeignKey(
        Preference_Genres,
        on_delete=models.CASCADE,
        verbose_name='preference_genre_id'
    )

    class Meta:
        db_table = 'User_Preference_Genres'


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
