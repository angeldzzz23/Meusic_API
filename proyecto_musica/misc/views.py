from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView


from rest_framework import response, status, permissions
from misc.serializers import AllGenresSerializer
from misc.serializers import GenresSerializer
from misc.serializers import SkillsSerializer
from misc.serializers import AllSkillsSerializer
from misc.serializers import  SpotifySerializer

from misc.models import Vimeo,Spotify,Youtube

# from misc.serializers import AllGenresSerializer

# Create your views here.

class SkillView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # make sure user is super admin
        # for testing pusposes I have it distabled
        user = request.user
        serializer = AllSkillsSerializer(user)


        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)

    def post(self, request):
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
        user = request.user
        serializer = AllGenresSerializer(user)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res)

    def post(self, request):
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

    # TODO: make sure that im only saving one
    def get(self, request):

        # handles the case of when there are no objects
        try:
            spot = Spotify.objects.all()[0]
        except:
            res = {'success' : True, 'data': {}}
            return response.Response(res, status=status.HTTP_201_CREATED)

        serializer=SpotifySerializer(spot)
        print(serializer.data)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


    # TODO: create get request to the spotify
    def post(self, request):
        jd = request.data
        if Spotify.objects.count() != 0:
            res = {'success' : False, 'error' : "there is already an obj"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # return error if body is too big
        serializer=SpotifySerializer(data=jd, context={"ss":"ss"})

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'message': serializer.error}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : True, 'data': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

    # TODO: create patch to edit
    def patch(self, request, id):
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
