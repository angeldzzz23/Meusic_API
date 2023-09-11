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
from api.models import Images, Videos



def validate_request(jd):
    if len(jd) != 2:
        res = {'success' : False, 'error': "you didnt add all of the parameters"}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

    if "title" not in jd:
        res = {'success' : False, 'error' : "Title has to be specified in the request as a key"}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

    if "image" not in jd:
    	res = {'success' : False, 'error' : "Image has to be specified in the request as a key"}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

    return None


def validate_image_title(jd):
    valid_titles = ["image_1","image_2","image_3","image_4","image_5","image_6", "profile_image"]

    if jd['title'] not in valid_titles:
        res = {'success' : False, 'error': "not a valid image title"}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

    return None


def deleteImage(img):
    if len(img) == 0:
        res = {'success' : False, 'error': 'image with that id does not exist'}
        return response.Response(res)

    imgeObj = img[0]
    imgeObj.image.delete()
    imgeObj.delete()
    return None


def deleteVideo(vid):
	if len(vid) == 0:
		res = {'success' : False, 'error': 'video with that id does not exist'}
   		return response.Response(res)

    videoObj = vid[0]
    videoObj.video.delete()
  	videoObj.delete()
  	return None


def postVideo(currentUsrVideo):
	if not currentUsrVideo:
    	res = {'success' : False, 'error' : "Request must contain video as a key."}
      	return response.Response(res, status=status.HTTP_400_BAD_REQUEST) 

    if len(currentUsrVideo) < 0:
        res = {'success' : False, 'error' : "Request must contain video as a key."}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

    return None






