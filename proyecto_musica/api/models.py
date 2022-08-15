# create user model

from django.db import models

class awsimage(models.Model):
    title = models.CharField(max_length=50)
    images = models.ImageField('image/')
