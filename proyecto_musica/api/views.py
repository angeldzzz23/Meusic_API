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

from api.models import Image
#pathlib.Path('save_path').mkdir(parents=True, exist_ok=True)
from proyecto_musica.settings import MEDIA_URL

# the picture serializer

from api.serializers import PictureSerialiser
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
    def get(self,request, id):
        #datos = {'codigo':"402",'message': "this is a get request..."}

        user_obj = User.objects.get(id="b0fdd4fec96b4d6ca3eacfbd2e713bd3")
        #img_objs = Image.objects.get(image_id=1)

        # this will give me the size of the object

        #img_objs2 = Image.objects.filter(user=user_obj, title=)
        #url = request.build_absolute_uri(img_objs2.image_1.url)
    #    newurl = str(url)

        datos = {'codigo':"200",'message': "this is a get request...", 'url': "newurl"}




        return JsonResponse(datos)


    # TODO:
    # renaming an image file
    # TODO: figure out a more efficient way to do this
    def post(self,request,id=None):
        serializer = self.serializer_class(data=request.data)
        jd = request.data


        # check if user added to
        if len(jd) != 2:
            datos = {'codigo':"404",'message': "you didnt add all of the parameters"}
            return JsonResponse(datos)

        # check if there is even an id
        if id is None:
            datos = {'codigo':"404",'message': "Bruh no user"}
            return JsonResponse(datos)

        # check if user exists
        # we would need to be logged in anyways
        try:
            user_obj = User.objects.get(id=id)
        except User.DoesNotExist:
            datos = {'codigo':"404",'message': "Bruh no a valid user"}
            return JsonResponse(datos)

        # make sure serializer is valid
        '''
        if serializer.is_valid():
            # implementation goes here

        else:
            # Return some error
            print("nah b")
        '''
        valid_titles = ["image_1","image_2","image_3","image_4","image_5","image_6", "profile_image"]
        # make sure title is valid

        if jd['title'] not in valid_titles:
            datos = {'codigo':"404",'message': "not a valid image name"}
            return JsonResponse(datos)


        # does the user already have an image_1, if they do then we
        CurrentUsrimages = Image.objects.filter(user=user_obj, title=jd['title'])

        if len(CurrentUsrimages) >= 1:
            datos = {'codigo':"404",'message': "You have already added " + jd['title'] }
            return JsonResponse(datos)

        else:
            # you add image to the user
            img = request.FILES["image"]
            newpic = Image(user=user_obj, title=jd['title'], image = img)
            newpic.save()
            # add url
            url = request.build_absolute_uri(newpic.image.url)
            newurl = str(url)
            newpic.url = newurl
            newpic.save()

            datos = {'codigo':"200",'message': "success", "url": newpic.url}
            return JsonResponse(datos)
