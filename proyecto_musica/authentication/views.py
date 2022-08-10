from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer
from authentication.serializers import EditSerializer
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
    serializer_class = EditSerializer

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        res = {'success' : True, 'user': serializer.data}
        return response.Response(res)

    def patch(self, request, id=None):
        jd = request.data

        try:
            user_obj = User.objects.get(id=id)
        except User.DoesNotExist:
            res = {'success' : False, 'error' : "User id does not exist."}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        if 'skills' in jd:
            skills = jd['skills']

            if not isinstance(skills, list):
                res = {'success' : False, 'error' : "Skills should be in a list."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            if len(skills) > 5:
                res = {'success' : False, 'error' : "Cannot submit more than 5 skills."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            if len(skills) != len(set(skills)):
                res = {'success' : False, 'error' : "Cannot submit duplicate skills."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            for skill in skills:
                if isinstance(skill, str) and (not skill.isnumeric()):
                    res = {'success' : False, 'error' : "Please enter numeric skills."}
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            for skill in skills:
                skill_from_db = Skills.objects.filter(skill_id=skill)
                if not skill_from_db:
                    res = {'success' : False, 'error' : "Skill not found in database."}
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            # delete exisiting entries
            User_Skills.objects.filter(user_id=id).delete()
            
            # add to User_Skills
            for skill in skills:    
                User_Skills.objects.create(user_id=id, skill_id=skill)
            
            serializer = EditSerializer(user_obj, data=request.data, 
                    context={'id': id, 'skills': skills}, partial=True)
        else:
            serializer = EditSerializer(user_obj, data=request.data, 
                    context={'id': id}, partial=True)

        if serializer.is_valid():
            serializer.save()

            serialized_data = serializer.data
            if serialized_data['skills'] is None:
                serialized_data.pop('skills')
           
            res = {'success' : True, 'user': serialized_data}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : False, 'user': serializer.errors}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(GenericAPIView):

    serializer_class= RegisterSerializer

    def post(self,request):
        jd = request.data

        if 'skills' in jd:
            # Error checking skills
            skills = jd['skills']
            if not isinstance(skills, list):
                res = {'success' : False, 'error' : "Skills should be in a list."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            if len(skills) > 5:
                res = {'success' : False, 'error' : "Cannot submit more than 5 skills."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            if len(skills) != len(set(skills)):
                res = {'success' : False, 'error' : "Cannot submit duplicate skills."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            for skill in skills:
                if isinstance(skill, str) and (not skill.isnumeric()):
                    res = {'success' : False, 'error' : "Please enter numeric skills."}
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            for skill in skills:
                skill_from_db = Skills.objects.filter(skill_id=skill)
                if not skill_from_db:
                    res = {'success' : False, 'error' : "Skill not found in database."}
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

            serializer = self.serializer_class(data=request.data, 
                         context={'skills': jd['skills']})
        else:
            serializer = self.serializer_class(data=request.data)

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
