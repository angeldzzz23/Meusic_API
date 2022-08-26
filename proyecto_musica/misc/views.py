from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView


from rest_framework import response, status, permissions
from misc.serializers import AllGenresSerializer
from misc.serializers import GenresSerializer
from misc.serializers import SkillsSerializer
from misc.serializers import AllSkillsSerializer
from misc.serializers import AllGendersSerializer
from misc.serializers import GendersSerializer

from misc.serializers import  SpotifySerializer, VimeoSerializer, YoutubeSerializer

from misc.models import Vimeo,Spotify,Youtube

# from misc.serializers import AllGenresSerializer

# Create your views here.

# TODO: clean up code  -  Angel
    # add helper method

# TODO: add sex View (I think you barely created this rashel, so once we can add)
class GenderView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # TODO: Add super user code

        # for testing pusposes I have it distabled
        user = request.user
        serializer = AllGendersSerializer(user)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)

    def post(self, request):
        
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to create objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        jd = request.data
        serializer = GendersSerializer(data=jd)
        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "something wrong with serializer"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class SkillView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # TODO: Add super user code

        # for testing pusposes I have it distabled
        user = request.user
        serializer = AllSkillsSerializer(user)


        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)

    def post(self, request):
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to create objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        jd = request.data
        serializer = SkillsSerializer(data=jd)
        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "something wrong with serializer"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)



class GenreView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # make sure user is super admin
        # for testing pusposes I have it distabled
        # TODO: Add super user code
        user = request.user
        serializer = AllGenresSerializer(user)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)

    def post(self, request):
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to create objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        jd = request.data
        serializer = GenresSerializer(data=jd)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "something wrong with serializer"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)


        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class SpotifyPlatforms(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # TODO: make sure that im only saving one
    def get(self, request):
        # TODO: Add super user code

        # handles the case of when there are no objects
        try:
            spot = Spotify.objects.all()[0]
        except:
            res = {'success' : True, 'data': {}}
            return response.Response(res, status=status.HTTP_201_CREATED)

        serializer=SpotifySerializer(spot)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


    # TODO: create get request to the spotify
    def post(self, request):
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to create objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        jd = request.data
        if Spotify.objects.count() != 0:
            res = {'success' : False, 'error' : "there is already an obj"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # return error if body is too big
        serializer=SpotifySerializer(data=jd, context={"ss":"ss"})

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'message': serializer.errors}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

    # TODO: create patch to edit
    def patch(self, request, id):
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        # checking if the id exists
        jd = request.data
        try:
            spot = Spotify.objects.get(spotify_id=id)
        except:
            res = {'success' : False, 'error' : "id does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=SpotifySerializer(spot,data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "invalid body requirements"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class VimeoPlatforms(GenericAPIView):
    def post(self, request):
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to create objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        jd = request.data
        if Vimeo.objects.count() != 0:
            res = {'success' : False, 'error' : "there is already an obj"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        # return error if body is too big
        serializer=VimeoSerializer(data=jd, context={"ss":"ss"})

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error': serializer.errors}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

    def get(self, request):
        # TODO: Add super user code
        # handles the case of when there are no objects
        try:
            spot = Vimeo.objects.all()[0]
        except:
            res = {'success' : True, 'data': {}}
            return response.Response(res, status=status.HTTP_201_CREATED)

        serializer=VimeoSerializer(spot)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

    # this takes the object id
    def patch(self, request, id):
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        jd = request.data
        try:
            vim = Vimeo.objects.get(vimeo_id=id)
        except:
            res = {'success' : False, 'error' : "id does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=VimeoSerializer(vim,data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "invalid body requirements"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

# this
class YoutubePlatforms(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    # takes care of the post
    def post(self, request):

        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to create objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        jd = request.data
        if Youtube.objects.count() != 0:
            res = {'success' : False, 'error' : "there is already an obj"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        # return error if body is too big
        serializer=YoutubeSerializer(data=jd, context={"ss":"ss"})

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error': serializer.errors}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

    def get(self, request):
        # TODO: Add super user code
        # handles the case of when there are no objects

        try:
            youtube = Youtube.objects.all()[0]
        except:
            res = {'success' : True, 'data': {}}
            return response.Response(res, status=status.HTTP_201_CREATED)

        serializer=YoutubeSerializer(youtube)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

        # this takes the object id
    def patch(self, request, id):
        jd = request.data

        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)


        try:
            you = Youtube.objects.get(youtube_id=id)
        except:
            res = {'success' : False, 'error' : "id does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=YoutubeSerializer(you,data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "invalid body requirements"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)
