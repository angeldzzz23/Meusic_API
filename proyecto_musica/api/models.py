# create user model
from django.shortcuts import render

from django.db import models
from authentication.models import User
from datetime import datetime

import random


# TODO: make cleaner
def get_uplaod_file_name(userpic, filename):
    ext = filename.split('.')[-1]
    newName = userpic.title + '.' + ext
    if userpic.title == "profile_image":
        return u'photos/%s/profileImg//%s' % (str(userpic.user.id),newName)
    return u'photos/%s/%s' % (str(userpic.user.id),newName)

def get_uplaod_video_name(userpic, filename):
    ext = filename.split('.')[-1]
    newName = userpic.title + '.' + ext
    if userpic.title == "profile_image":
        return u'videos/%s/vids//%s' % (str(userpic.user.id),newName)
    return u'videos/%s/%s' % (str(userpic.user.id),newName)

# these are the images for the profile page
    # image_1
    # image_2
    # image_3
    # image_4
    # image_5
    # image_6
# Profile_image
    # profile_image



# change name of image_One

class Images(models.Model):
    image_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='image_id'
  )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='user_id'
   )

    url = models.URLField(max_length = 200, null=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=get_uplaod_file_name)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Images'

class Videos(models.Model):
    video_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        null=False,
        verbose_name='video_id'
  )

    user = models.ForeignKey(
          User,
          on_delete=models.CASCADE,
          verbose_name='user_id'
     )

    url = models.URLField(max_length = 200, null=True)
    title = models.CharField(max_length=50)
    caption = models.CharField(max_length=300, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to=get_uplaod_video_name)





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


# imagen 1

# iimage 2

# iimage 3

# imagen_5

# iimage 5


# When updating I would have to image

# TODO: Validate the max amount permitted



'''
 class Video:
    multimedia_id
    user_id

    title = models.CharField(max_length=50)
    video = models.Video('video/')
'''



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
