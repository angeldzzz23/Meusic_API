from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from authentication.models import User
from Cprofile.serializers import CSkills, CGenres



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
