from django.shortcuts import render

import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from search.serializers import GenderSerializer, SkillsSerializer, GenresSerializer
from rest_framework import filters
from rest_framework import generics


from rest_framework import response, status, permissions
from authentication.models import Genders,Skills,Genres


# Create your views here.

# searching the gender
class SearchGender(generics.ListCreateAPIView):
    search_fields = ['gender_name']
    filter_backends = (filters.SearchFilter,)
    queryset = Genders.objects.all()
    serializer_class = GenderSerializer


class searchSkills(generics.ListCreateAPIView):
    search_fields = ['skill_name']
    filter_backends = (filters.SearchFilter,)
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer

class searchGenres(generics.ListCreateAPIView):
    search_fields = ['genre_name']
    filter_backends = (filters.SearchFilter,)
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


# searching the skills
