from django.shortcuts import render

import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView


from rest_framework import response, status, permissions

# Create your views here.


class SearchGender(GenericAPIView):
    def get(self, request):
        res = {'success' : True, 'data': "serializer.data"}
        return response.Response(res)
