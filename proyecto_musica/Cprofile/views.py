from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from authentication.models import User
from Cprofile.serializers import CSkills, CGenres, CArtist, CYoutubeVids, CVimeoVids

# this contains a bunch of

class CUserSkills(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}

        serializer = CSkills(user)

        res = {}
        res['success'] = True
        res['skills'] = serializer.data['skills']

        return JsonResponse(res)


# this gets all of the user's favorite genres
class CUserGenres(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}

        serializer = CGenres(user)

        res = {}
        res['success'] = True
        res['genres'] = serializer.data['genres']

        return JsonResponse(res)

# this gets all of the user artists.
class CUserArtists(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}

        serializer = CArtist(user)

        res = {}
        res['success'] = True
        res['artists'] = serializer.data['artists']

        return JsonResponse(res)


class CUserYoutubeVideos(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}

        serializer = CYoutubeVids(user)

        res = {}
        res['success'] = True
        res['youtube_vids'] = serializer.data['youtube_vids']

        return JsonResponse(res)


class CUserVimeoVideos(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}

        serializer = CVimeoVids(user)

        res = {}
        res['success'] = True
        res['vimeo_vids'] = serializer.data['vimeo_vids']

        return JsonResponse(res)
