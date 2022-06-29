from django.db import models
from django.contrib.auth.models import AbstractBaseUser # standard base classes
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

from django.db import models
import uuid





# Create your models here.
class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """

    def create_user(self, email, password=None):
        """ Create a new user profile"""
        if not email: # raise an exeption
            raise ValueError('users must have an email address')
        #normalizing an email addresss
        email = self.normalize_email(email)
        user = self.model(email=email,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """ Create and save a new superuser with given details """

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Gender(models.Model):
    gender_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='gender_id')
    gender_description = models.CharField(max_length=200)
    def __str__(self):
        return self.gender_id
    class Meta:
        db_table = 'Gender'

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True,editable=False)
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255,default='')
    last_name = models.CharField(max_length=100,default='')
    gender =models.ForeignKey(Gender, on_delete=models.CASCADE,verbose_name='gender_id',default='1')
    account_created= models.DateTimeField( auto_now_add = True)
    about_me = models.CharField(max_length=250, default=' ')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects =  UserProfileManager()

    # both email and name are required
    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """ Reteieve short name of user"""
        return self.name

    # this is recommended for all django models
    def __str__(self):
        """Return string representation of our user """
        return self.email

### this creates a new feed update item
class ProfileFeedItem(models.Model):
    """Profile status update"""

    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    status_text = models.CharField(max_length=255)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
