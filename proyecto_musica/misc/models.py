from django.db import models

# Create your models here.



# add the vimeo model
class Vimeo(models.Model):
    vimeo_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='vimeo_id')
    client_id =models.CharField(max_length=255)
    client_secret =models.CharField(max_length=255)
    class Meta:
        db_table = 'vimeo'


# Add the spotify Model
class Spotify(models.Model):
    spotify_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='spotify_id')
    client_id =models.CharField(max_length=255)
    client_secret =models.CharField(max_length=255)
    class Meta:
        db_table = 'spotify'

# add the youtube model
class Youtube(models.Model):
    youtube_id=models.BigAutoField(auto_created=True, primary_key=True,unique=True,null=False,verbose_name='youtube_id')
    key=models.CharField(max_length=255)
    class Meta:
        db_table = 'youtube'
