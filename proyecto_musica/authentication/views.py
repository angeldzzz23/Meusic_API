from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer
from authentication.serializers import LoginSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from authentication.models import User, User_Skills, Skills

import json

# TODO: implement the edit user functionality - patch
# TODO: implement delete user functionality

# Create your views here.


class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})


class RegisterAPIView(GenericAPIView):

    serializer_class= RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        # send data to serializer to turn json data into python objects

        if serializer.is_valid():
            serializer.save()

            # TODO rashel: do i need to serialize the data? check serializers.py...
            jd = request.data
            if 'skill_1' in jd:
                user = User.objects.get(email=jd['email'])
                skill = Skills.objects.get(skill_id=jd['skill_1'])
                User_Skills.objects.create(user=user,skill=skill)
            if 'skill_2' in jd:
                user = User.objects.get(email=jd['email'])
                skill = Skills.objects.get(skill_id=jd['skill_2'])
                User_Skills.objects.create(user=user,skill=skill)
            if 'skill_3' in jd:
                user = User.objects.get(email=jd['email'])
                skill = Skills.objects.get(skill_id=jd['skill_3'])
                User_Skills.objects.create(user=user,skill=skill)
            if 'skill_4' in jd:
                user = User.objects.get(email=jd['email'])
                skill = Skills.objects.get(skill_id=jd['skill_4'])
                User_Skills.objects.create(user=user,skill=skill)
            if 'skill_5' in jd:
                user = User.objects.get(email=jd['email'])
                skill = Skills.objects.get(skill_id=jd['skill_5'])
                User_Skills.objects.create(user=user,skill=skill)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# this used to log in the user
# response gives us the token if it is a valid login
class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class= LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user=authenticate(username=email, password=password)

        if user:
            serializer=self.serializer_class(user)

            return response.Response(serializer.data, status.HTTP_200_OK)

        return response.Response({'message': "invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
