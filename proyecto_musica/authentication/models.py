from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
    PermissionsMixin, UserManager, AbstractBaseUser)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from datetime import datetime, timedelta

import jwt
import uuid

from django.conf import settings

# Create your models here.

# modify me Rashel
class MyUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    id=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True,null=False,verbose_name='user_id')

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified = models.BooleanField(
        _('email_verified'),
        default=False,
        help_text=_(
            'Designates whether this users email is verified. '

        ),
    )
    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # this returns a token that expires in 24 hours
    @property
    def token(self):
        token = jwt.encode(
            {'id': str(self.id),
                'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')

        return token


class Skills(models.Model):
    skill_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='skill_id',
    )
    skill_name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.skill_id
    class Meta:
        db_table = 'Skills'


class User_Skills(models.Model):
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
    skill = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='skill_id'
    )

    class Meta:
        db_table = 'User_Skills'


class Genres(models.Model):
    genre_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='genre_id',
    )
    genre_name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.genre_id
    class Meta:
        db_table = 'Genres'


class User_Genres(models.Model):
    user_genre_id = models.BigAutoField(
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
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='genre_id'
    )

    class Meta:
        db_table = 'User_Genres'


class User_Artists(models.Model):
    user_artist_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='user_artist_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )
    artist = models.IntegerField(
        verbose_name='artist_id'
    )

    class Meta:
        db_table = 'User_Artists'


class Genders(models.Model):
    gender_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='gender_id',
    )
    gender_name = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.gender_id
    class Meta:
        db_table = 'Genders'

