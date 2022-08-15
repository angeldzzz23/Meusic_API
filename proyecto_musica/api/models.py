# create user model

from django.db import models
from authentication.models import User

# this contains all of the types of media that we can have
class Multimedia_type(models.Model):

    multimedia_type_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='multimedia_type_id',
    )

    multimedia_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.multimedia_type_id

    class Meta:
        db_table = 'Multimedia_type'

# status multimedia of the multimedia
# ex. visible, hidden, deleted
class Multimedia_status(models.Model):
    multimedia_status_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='multimedia_status_id',
    )
    multimedia_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.multimedia_status_id
    class Meta:
        db_table = 'Multimedia_status'


# this contains the type of formats that we allow the user to enter
class Format(models.Model):
    format_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='format_id',
    )
    format_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.format_id
    class Meta:
        db_table = 'Format'

# this is table is where we save all of our user multimedia files that are uploade
class Multimedia(models.Model):

    multimedia_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='multimedia_id'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
    )

    multimedia_type = models.ForeignKey(
        Multimedia_type,
        on_delete=models.CASCADE,
        verbose_name='multimedia_type_id'
    )

    format = models.ForeignKey(
        Format,
        on_delete=models.CASCADE,
        verbose_name='format_id'
    )

    url = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    description = models.CharField(max_length=200)

    multimedia_status = models.ForeignKey(
        Multimedia_status,
        on_delete=models.CASCADE,
        verbose_name='multimedia_status_id'
    )

    def __str__(self):
        return self.multimedia_id
    class Meta:
        db_table = 'Multimedia'
