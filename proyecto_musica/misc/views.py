from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView

from rest_framework import response, status, permissions
from misc.serializers import SkillsSerializer
from misc.serializers import AllSkillsSerializer


# Create your views here.
class GenresView(GenericAPIView):
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
            print("nagh")


        datos = {'codigo':"400",'data': serializer.data}
        return JsonResponse(datos)
