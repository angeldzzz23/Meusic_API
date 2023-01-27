from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from authentication.models import User
from Cprofile.serializers import CSkills, CGenres, CArtist, CYoutubeVids, CVimeoVids, CPersonalVideo, CPersonalPictures, CPersonalInfo, CusernameInfo, CTheNameOfUser, CDOBOfUser, CGender, Cnationalities

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



class CUserPersonalVideos(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}

        serializer = CPersonalVideo(user)

        res = {}
        res['success'] = True
        res['video'] = serializer.data['video']

        return JsonResponse(res)


#

class CUserPersonalImages(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}

        serializer = CPersonalPictures(user)

        res = {}
        res['success'] = True
        res['pictures'] = serializer.data['pictures']

        return JsonResponse(res)

    # getting the name of the user

# getting the gender
class CUserGender(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        jd = request.data
        user = request.user
        context = {}

        serializer = CGender(user)

        res = {}
        res['success'] = True
        res['gender_name'] = serializer.data['gender_name']


        return JsonResponse(res)




class CUserAboutMe(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        jd = request.data
        user = request.user
        context = {}

        serializer = CPersonalInfo(user)

        res = {}
        res['success'] = True
        res['about_me'] = serializer.data['about_me']


        return JsonResponse(res)


class CUsername(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        jd = request.data
        user = request.user
        context = {}

        serializer = CusernameInfo(user)

        res = {}
        res['success'] = True
        res['username'] = serializer.data['username']


        return JsonResponse(res)


# CTheNameOfUser

class Cname(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        jd = request.data
        user = request.user
        context = {}

        serializer = CTheNameOfUser(user)

        res = {}
        res['success'] = True
        res['first_name'] = serializer.data['first_name']
        res['last_name'] = serializer.data['last_name']

        return JsonResponse(res)


class Cdob(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        jd = request.data
        user = request.user
        context = {}

        serializer = CDOBOfUser(user)

        res = {}
        res['success'] = True
        res['DOB'] = serializer.data['DOB']

        return JsonResponse(res)

# getting the nationalities of the user
#

class Cnationality(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)


    def get(self, request):
        # Cnationalities
        jd = request.data
        user = request.user
        context = {}
        serializer = Cnationalities(user)

        res = {}
        res['Success'] = True
        res['nationalities'] = serializer.data['nationality']

        return JsonResponse(res)
