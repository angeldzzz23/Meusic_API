#from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.views import View
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os
from django.shortcuts import render
import json
from authentication.models import User
import pathlib
from PIL import Image
from django.core import serializers




from api.models import Images, Videos
#pathlib.Path('save_path').mkdir(parents=True, exist_ok=True)
from proyecto_musica.settings import MEDIA_URL

# the picture serializer

from api.serializers import PictureSerialiser
from api.serializers import PicturesSerializer
from api.serializers import Videoerialiser
from api.serializers import VideosSerializer

from rest_framework import response, status, permissions



#import mimetypes
#from django.http import HttpResponse
#from rest_framework import response, status, permissions
#from django.contrib.auth import authenticate

# add
# TODO: add an update method

class UpdateImage(GenericAPIView):

    serializer_class= PictureSerialiser
    permission_classes = (permissions.IsAuthenticated,)

    # create serializer
    # TODO: Ignore messy code

    # this returns all of the imags that bellong to a user

    def get(self,request):
        user = request.user
        serializer = PicturesSerializer(user)
        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)


    # deleting the image
    def delete(self, request,id=None):
        user = request.user
        img = Images.objects.filter(image_id=id, user=request.user.id)

        if len(img) == 0:
            res = {'success' : False, 'error': 'video with that id does not exist'}
            return response.Response(res)

        imgeObj = img[0]
        imgeObj.image.delete()
        imgeObj.delete()



        serializer = PicturesSerializer(user)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)


    # this post method requires an id
    # creates an an image record for the user
        # in the case of when the user already has an image saved in the specific spot
            # we override the image
    def post(self,request,id=None):
        jd = request.data

        #making sure that the body is only 2
        if len(jd) != 2:
            res = {'success' : False, 'error': "you didnt add all of the parameters"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        #verifying that we have a valid user
        try:
            user_obj = request.user
        except User.DoesNotExist:
            res = {'success' : False, 'error' : "User id does not exist."}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # verify that im uploadin a valid image
        img = request.FILES["image"]

        try:
            trial_image = Image.open(img)
            a = trial_image.verify()
        except :
            res = {'success' : False, 'error' : "not a valid image format"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        newpic = Images(user=user_obj, title=jd['title'], image = img)
        # TODO: imeplement enums
        valid_titles = ["image_1","image_2","image_3","image_4","image_5","image_6", "profile_image"]

        # making sure that we have a valid title name
        if jd['title'] not in valid_titles:
            res = {'success' : False, 'error': "not a valid image type"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # does the user already have an image_1, if they do then we
        CurrentUsrimages = Images.objects.filter(user=user_obj, title=jd['title'])

        picture_serializer = PictureSerialiser(data=jd, context={'user': user_obj, 'img' : img, 'request': request})

        if picture_serializer.is_valid():
            # implementation goes here
            picture_serializer.save()
            datos = {'success':True,'data':picture_serializer.data}

            return response.Response(datos, status=status.HTTP_201_CREATED)
        else:
                datos = {'codigo':"200",'message': "success", "url": newpic.url}
                return JsonResponse(datos)

class UpdateVideo(GenericAPIView):
        serializer_class= PictureSerialiser
        permission_classes = (permissions.IsAuthenticated,)


        def get(self,request):
            user = request.user
            serializer = VideosSerializer(user)
            res = {'success' : True, 'data': serializer.data}
            return response.Response(res)


        # adding the delete methodb

        def delete(self, request, id=None):
            vid = Videos.objects.filter(video_id=id, user=request.user.id)


            if len(vid) == 0:
                res = {'success' : False, 'error': 'video with that id does not exist'}
                return response.Response(res)

            videoObj = vid[0]
            videoObj.video.delete()
            videoObj.delete()

            res = {'success' : True, 'videos': []}

            return response.Response(res)

        # im only going to allow intro Videos
        def post(self,request,id=None):
            jd = request.data

            try:
                user_obj = request.user
            except User.DoesNotExist:
                res = {'success' : False, 'error' : "User id does not exist."}
                return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

            video = request.FILES["video"]

            # here we should check if the image is a video
            if video:
                filename = video.name

                if  (filename.endswith('.MP4') or filename.endswith('.mp4')) == False :
                    datos = {'success':False,'data':"file is not of type .mp4"}
                    return response.Response(datos, status=status.HTTP_201_CREATED)

            video_serializer = Videoerialiser(data=jd, context={'user': user_obj, 'vid' : video, 'request': request})

            if video_serializer.is_valid():
                video_serializer.save()
                datos = {'success':True,'data':video_serializer.data}
                return response.Response(datos, status=status.HTTP_201_CREATED)
            else:
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            res = {'success' : True, 'data': "serializer.data"}
            return response.Response(res)
