from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from rest_framework import response
from authentication.models import User
from authentication.serializers import RegisterSerializer

# importing the serialziers
from newsfeed.serializers import ProfileSerializer


# this is in charge of showing the profile of the user
# user needs to be logged in.
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

        del serialized_data['email']
        # del serialized_data['user']['email']


        res = {'success' : True, 'user': serialized_data}

        return response.Response(res, status=status.HTTP_201_CREATED)


# this will get the profile of the user.
class SeeUserView(GenericAPIView):
    # where id is the username
    # if the user does not have a valid username, then
    def get(self, request,id):

        try:
            user = User.objects.get(username=id)

        except User.DoesNotExist:
            res = {'success' : True, 'user': None}
            return response.Response(res, status=status.HTTP_200_OK)

        serializer = ProfileSerializer(user)

        # make sure there is a profile image and a a video at least
        serialized_data = serializer.data


        if serialized_data['pictures'] == None or serialized_data['video'] == None:
            res = {'success' : True, 'user': None}
            return response.Response(res, status=status.HTTP_200_OK)

        res = {'success' : True, 'user': serialized_data}

        return response.Response(res, status=status.HTTP_200_OK)


# the newsfeed
# this will get the feed view
class Feed(GenericAPIView):

    def get(self, request):
         res = {'ahaha': "hello world"}


         return response.Response(res, status=status.HTTP_200_OK)
