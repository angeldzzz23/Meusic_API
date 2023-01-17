from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView


from rest_framework import response


class SeeProfileOfUserView(GenericAPIView):


    def get(self, request,id):
        print(id)

        datos = {'codigo':"200",'message': "Users not found..."}
        return JsonResponse(datos)
        esponse.Response(datos, status=status.HTTP_201_CREATED)
