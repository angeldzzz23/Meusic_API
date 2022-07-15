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

    def _create_user(self, username, email, password, skill_1=None,**extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')


        if not skill_1:
            raise ValueError('no skill 1')


        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email,skill_1=skill_1, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # LOOOK at me gooooooo Rashel!!!
        # you might want to put this in views.py
        # this should only be done if an account is created
        # an accoutn shouldnt be created if any of the skills doesnt exist
        if skill_1 is not None:
            user_id = User.objects.filter(username=username).values('id')
            User_Skills.objects.create(user=user,skill=skill_1)



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


class Skills(models.Model):
    skill_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='skill_id',
    )
    skill_name = models.CharField(max_length=200)

    def __str__(self):
        return self.skill_id
    class Meta:
        db_table = 'Skills'


# modify me Rashel
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
    skill_1 = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='skill_1_id',
        related_name='skill_1',
        null=True,
    )
    skill_2 = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='skill_2_id',
        related_name='skill_2',
        null=True,
    )
    skill_3 = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='skill_3_id',
        related_name='skill_3',
        null=True,
    )
    skill_4 = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='skill_4_id',
        related_name='skill_4',
        null=True,
    )
    skill_5 = models.ForeignKey(
        Skills,
        on_delete=models.CASCADE,
        verbose_name='skill_5_id',
        related_name='skill_5',
        null=True,
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


    '''def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.id is None:
            if self.skill_1 is not None:
                user_obj = User.objects.get(id=self.id)
                user_skill = User_Skills(user=user_obj, skill=self.skill_1)
                user_skill.save()'''


    # this returns a token that expires in 24 hours
    @property
    def token(self):
        token = jwt.encode(
            {'username': self.username, 'email': self.email,
                'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')

        return token


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
