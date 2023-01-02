from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView


from rest_framework import response, status, permissions



class CUserSkills(GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):

        datos = {'codigo':"400",'message': "El correo electronico ya existe"}
        return JsonResponse(datos)
