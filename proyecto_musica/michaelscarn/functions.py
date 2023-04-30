from authentication.models import User, Skills, User_Skills, Genres, User_Genres, User_Artists, User_Youtube, User_Vimeo, Nationality, User_Nationality, User_Videos
from rest_framework import response, status
from enum import Enum
import re
from api.models import Images
from api.models import Videos
import os
from proyecto_musica.settings import BASE_DIR
from pathlib import Path
import shutil

def deleteUser(id):
    # deleting the user
    User_Genres.objects.filter(user_id=id).delete()
    User_Skills.objects.filter(user_id=id).delete()
    User_Artists.objects.filter(user_id=id).delete()
    User_Nationality.objects.filter(user_id=id).delete()

    # deleting the pics
    pics = Images.objects.filter(user_id=id)


    for pic in pics:
        pic.image.delete()
        pic.delete()

    # deleting the videos
    vids = Videos.objects.filter(user_id=id)

    for video in vids:
        video.video.delete()
        video.delete()


    # TODO: delete its media folder
    file_location = os.path.join(BASE_DIR, 'media/videos/' + str(id))
    p = Path(file_location)
    if p.is_dir():
        shutil.rmtree(file_location, ignore_errors = False)



    # deletes image folder
    # delete its images folder
    file_location = os.path.join(BASE_DIR, 'media/photos/' + str(id))
    p = Path(file_location)

    if p.is_dir():
        shutil.rmtree(file_location, ignore_errors = False)

    #delete user
    usr = User.objects.get(id = id)
    usr.delete()


