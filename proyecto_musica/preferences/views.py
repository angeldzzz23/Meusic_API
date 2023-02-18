from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions

from preferences.serializers import PreferenceGendersSerializer, PreferenceSkillsSerializer, PreferenceGenresSerializer

from preferences.serializers import PreferenceAgeSerializer
from preferences.serializers import PreferenceDistanceSerializer
from preferences.serializers import PreferenceGloballySerializer
from preferences.serializers import PreferenceEditSerializer

from authentication.models import Genders, Genres, Skills, User
from preferences.models import User_Preference_Genders, User_Preference_Skills, User_Preference_Genres
from preferences.models import User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
from preferences.functions import User_Fields, get_list_field, List_Fields, validate_field

class PreferenceGenderView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}
        serializer = PreferenceGendersSerializer(user)
        res = {}
        res['success'] = True
        res['genders'] = serializer.data['genders']
        return response.Response(res, status=status.HTTP_200_OK)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceGendersSerializer(data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "invalid body requirements"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'gender': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class PreferenceSkillView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}
        serializer = PreferenceSkillsSerializer(user)
        res = {}
        res['success'] = True
        res['skills'] = serializer.data['skills']
        return response.Response(res, status=status.HTTP_200_OK)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceSkillsSerializer(data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : serializer.errors}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'skill': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class PreferenceGenreView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}
        serializer = PreferenceGenresSerializer(user)
        res = {}
        res['success'] = True
        res['genres'] = serializer.data['genres']
        return response.Response(res, status=status.HTTP_200_OK)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceGenresSerializer(data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : serializer.errors}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'genre': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)

class PreferenceAgeView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}
        serializer = PreferenceAgeSerializer(user)
        res = {}
        res['success'] = True
        res['age'] = serializer.data['age']
        return response.Response(res, status=status.HTTP_200_OK)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceAgeSerializer(data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "invalid body requirements"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'age': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class PreferenceDistanceView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}
        serializer = PreferenceDistanceSerializer(user)
        res = {}
        res['success'] = True
        res['distance'] = serializer.data['distance']
        return response.Response(res, status=status.HTTP_200_OK)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceDistanceSerializer(data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "invalid body requirements"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'distance': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class PreferenceGloballyView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        jd = request.data
        user = request.user
        context = {}
        serializer = PreferenceGloballySerializer(user)
        res = {}
        res['success'] = True
        res['search_globally'] = serializer.data['search_globally']
        return response.Response(res, status=status.HTTP_200_OK)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceGloballySerializer(data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : "invalid body requirements"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'search_globally': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)



class PreferenceUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PreferenceEditSerializer

    def get(self, request):
        print("get request")
        user = request.user
        serializer = PreferenceEditSerializer(user)
        serialized_data = serializer.data

        res = {'success' : True, 'preferences': serialized_data}
        return response.Response(res)

    def patch(self, request):
        jd = request.data
        id = request.user.id
        context = {}
        try:
            user_obj = User.objects.get(id=id)
        except User.DoesNotExist:
            res = {'success' : False, 'error' : "User id does not exist."}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        request_keys = list(jd.keys())
        allowed_keys = [e.value for e in User_Fields]

        for key in request_keys:
            if key not in allowed_keys:
                res = {'success' : False,
                        'error' : "Wrong parameter(s) passed in request."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)


        #Validation of list field
        for field in List_Fields:
            field_name = field.value
            #print(field_name) prints skills, genres as field name
            if field_name in jd:
                field_list = jd[field_name]
                res = validate_field(field_name, field_list)
                if res:
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)
                context[field_name] = field_list


        print('jd', jd)
        print('context', context)
        print('user object', user_obj)

        serializer = PreferenceEditSerializer(user_obj, data=jd,
                                           context=context, partial=True)

        if serializer.is_valid():
            serializer.save()
            # only return fields that were modified
            serialized_data = (serializer.data).copy()
            for field in serializer.data:
                if field not in jd:
                    serialized_data.pop(field)


            res = {'success' : True, 'preferences': serialized_data}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : False, 'preferences': serializer.errors}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
