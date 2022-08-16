from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer
from authentication.serializers import EditSerializer
from authentication.serializers import LoginSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from authentication.models import User, User_Skills, Skills, Genres, User_Genres
from authentication.functions import validate_field, List_Fields

import json


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
            validate_field("skill", skills)

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
        context = {}

        for field in List_Fields:
            field_name = field.value
            
            if field_name in jd:
                field_list = jd[field_name]
                res = validate_field(field_name, field_list)
                if res:
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)
                context[field_name] = field_list

        serializer = self.serializer_class(data=jd, 
                                           context=context)

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
