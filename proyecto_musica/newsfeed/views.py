from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions

from rest_framework import response

from authentication.models import User
from authentication.serializers import RegisterSerializer


class SeeProfileOfUserView(GenericAPIView):

    # this returns the public profile of a user in the newsfeed
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request,id):

        try:
            user = User.objects.get(username=id)

        except User.DoesNotExist:
            res = {'success' : True, 'user': None}
            return response.Response(res, status=status.HTTP_200_OK)


        serializer = RegisterSerializer(user)
        serialized_data = (serializer.data).copy()
        if 'gender' in serializer.data:
            serialized_data.pop('gender')

        res = {'success' : True, 'user': serialized_data}

        return response.Response(res, status=status.HTTP_201_CREATED)
