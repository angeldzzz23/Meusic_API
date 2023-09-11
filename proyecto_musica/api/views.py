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
from proyecto_musica.settings import MEDIA_URL
from api.serializers import PictureSerialiser
from api.serializers import PicturesSerializer
from api.serializers import Videoerialiser
from api.serializers import VideosSerializer
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView
from ranged_fileresponse import RangedFileResponse
from django.conf import settings
import os
from api.functions import validate_request, validate_image_title, deleteImage, deleteVideo, postVideo



class UpdateImage(GenericAPIView):
    serializer_class= PictureSerialiser
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        user = request.user
        serializer = PicturesSerializer(user)
        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)


    def delete(self, request,id=None):
        user = request.user
        img = Images.objects.filter(image_id=id, user=request.user.id)
        deleteImageResponse = deleteImage(img)
        if deleteImageResponse is not None: return deleteImageResponse

        serializer = PicturesSerializer(user)
        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)


    def post(self,request,id=None):
        jd = request.data
        validData = functions.validate_request(jd)
        if validData is not None: return validData

        try:
            user_obj = request.user
        except User.DoesNotExist:
            res = {'success' : False, 'error' : "User id does not exist."}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        img = request.FILES["image"]

        try:
            trial_image = Image.open(img)
            a = trial_image.verify()
        except :
            res = {'success' : False, 'error' : "not a valid image format"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        newpic = Images(user=user_obj, title=jd['title'], image = img)
        validDataImage = validate_image_title(jd)
        if validDataImage is not None: return validDataImage

        CurrentUsrimages = Images.objects.filter(user=user_obj, title=jd['title'])
        picture_serializer = PictureSerialiser(data=jd, context={'user': user_obj, 'img' : img, 'request': request})
        if picture_serializer.is_valid():
            picture_serializer.save()
            datos = {'success':True,'data':picture_serializer.data}
            return response.Response(datos, status=status.HTTP_201_CREATED)
        else:
            datos = {'codigo':"200",'message': "success", "url": newpic.url}
            return JsonResponse(datos)


class LoadVideo(GenericAPIView): 
    def get(self, request): 
        video_path = "sample_vid.mp4" 
        file_size = os.path.getsize(video_path)
        response = RangedFileResponse(request, open(video_path, "rb"), content_type="video/mp4")
        return response

class UpdateVideo(GenericAPIView):
        serializer_class= PictureSerialiser
        permission_classes = (permissions.IsAuthenticated,)
        def get(self,request):
            user = request.user
            serializer = VideosSerializer(user)
            res = {}
            res['success'] = True
            res['videos'] = serializer.data['videos']
            res = res
            return response.Response(res)


        def delete(self, request, id=None):
            vid = Videos.objects.filter(video_id=id, user=request.user.id)
            deleteVideoResponse = deleteVideo(vid)
            if deleteVideoResponse is not None: return deleteVideoResponse
            res = {'success' : True, 'videos': []}
            return response.Response(res)


        def post(self,request,id=None):
            jd = request.data
            caption = None
            if 'caption' in jd:
                caption = jd['caption']

            try:
                user_obj = request.user
            except User.DoesNotExist:
                res = {'success' : False, 'error' : "User id does not exist."}
                return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

    
            if "video" not in jd:
                currentUsrVideo = Videos.objects.filter(user=request.user)
                postVideoResponse = postVideo(currentUsrVideo)
                if postVideoResponse is not None: return postVideoResponse
                else:                    
                    currentUsrVideo[0].caption = caption
                    currentUsrVideo[0].save()
                    serializer = VideosSerializer(request.user)
                    res = {}
                    res['success'] = True
                    res['video'] = serializer.data['videos'][0]
                    del res['video']['title'] 
                    res = res
                    return response.Response(res)

                res = {'success' : False, 'error' : "Request must contain video as a key."}
                return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

            video = request.FILES["video"]
            if video:
                filename = video.name

                if  (filename.endswith('.MP4') or filename.endswith('.mp4')) == False :
                    datos = {'success':False,'data':"file is not of type .mp4"}
                    return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)


            video_serializer = Videoerialiser(data=jd, context={'user': user_obj, 'vid' : video, 'request': request, 'caption': caption})
            if video_serializer.is_valid():
                video_serializer.save()
                res = {}
                res['success'] = True
                res['video'] = video_serializer.data
                datos = res
                return response.Response(datos, status=status.HTTP_201_CREATED)
            else:
                datos = {'success':True,'data':video_serializer.errors}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            res = {'success' : True, 'data': "serializer.data"}
            return response.Response(res)
