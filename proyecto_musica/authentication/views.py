from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer
from authentication.serializers import SkillsSerializer
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
    serializer_class = SkillsSerializer

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response({'user': serializer.data})

    def patch(self, request, id=None):
        jd = request.data
        user_obj = User.objects.get(id=id)

        # edge case: if user passes in wrong type of input (list of strings instead, an integer), what happens?
        if 'skills' in jd:
            skills = jd['skills']

            if len(skills) > 5:
                message = {'message': "Cannot submit more than 5 skills."}
                return response.Response(message, status=status.HTTP_401_UNAUTHORIZED)

            for skill in skills:
                skill_from_db = Skills.objects.filter(skill_id=skill)
                if not skill_from_db:
                    message = {'message': "Skill not found in database"}
                    return response.Response(message, status=status.HTTP_401_UNAUTHORIZED)

            # delete exisiting entries
            User_Skills.objects.filter(user_id=id).delete()
            
            # add to User_Skills
            for skill in skills:    
                User_Skills.objects.create(user_id=id, skill_id=skill)
            
            serializer = SkillsSerializer(user_obj, data=request.data, 
                    context={'id': id, 'skills': skills}, partial=True)
        else:
            serializer = SkillsSerializer(user_obj, data=request.data, 
                    context={'id': id}, partial=True)

        if serializer.is_valid():
            serializer.save()

            serialized_data = serializer.data
            if serialized_data['skills'] is None:
                serialized_data.pop('skills')
            
            return response.Response(serialized_data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(GenericAPIView):

    serializer_class= RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        # send data to serializer to turn json data into python objects

        if serializer.is_valid():
            serializer.save()
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
