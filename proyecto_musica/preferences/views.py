from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions

from preferences.serializers import PreferenceGendersSerializer
from preferences.serializers import AllPreferenceGendersSerializer
from preferences.serializers import PreferenceSkillsSerializer
from preferences.serializers import AllPreferenceSkillsSerializer
from preferences.serializers import PreferenceGenresSerializer
from preferences.serializers import AllPreferenceGenresSerializer
from preferences.serializers import PreferenceAgeSerializer
from preferences.serializers import PreferenceDistanceSerializer
from preferences.serializers import EditPreferenceSerializer


from preferences.models import Preference_Genders, User_Preference_Genders
from preferences.models import Preference_Skills, User_Preference_Skills
from preferences.models import Preference_Genres, User_Preference_Genres
from preferences.models import User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally

class PreferenceGenderView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        # for testing pusposes I have it distabled
        user = request.user
        serializer = AllPreferenceGendersSerializer(user)

        jd = {'success' : True}
        jd.update(serializer.data)

        res = jd
        return response.Response(res)



    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     you = Preference_Genders.objects.get(preference_gender_id=id)

        # except:
        #     res = {'success' : False, 'error' : "id does not exist"}
        #     return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

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
        user = request.user
        serializer = AllPreferenceSkillsSerializer(user)
        jd = {'success' : True}
        jd.update(serializer.data)
        res = jd
        return response.Response(res)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     you = Preference_Skills.objects.get(preference_skill_id=id)

        # except:
        #     res = {'success' : False, 'error' : "id does not exist"}
        #     return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

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
        # make sure user is super admin
        # for testing pusposes I have it distabled
        # TODO: Add super user code
        user = request.user
        serializer = AllPreferenceGenresSerializer(user)
        jd = {'success' : True}
        jd.update(serializer.data)
        res = jd
        return response.Response(res)


    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     you = Preference_Genres.objects.get(preference_genre_id=id)

        # except:
        #     res = {'success' : False, 'error' : "id does not exist"}
        #     return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

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
        user = request.user
        serializer = PreferenceAgeSerializer(user)
        jd = {'success' : True}
        jd.update(serializer.data)
        res = jd
        return response.Response(res)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     you = User_Preferences_Age.objects.get(preference_age_id=id)
        # except:
        #     res = {'success' : False, 'error' : "id does not exist"}
        #     return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        serializer=PreferenceAgeSerializer(data=jd,partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : serializer.errors}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        res = {'success' : True, 'age': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)



class PreferenceDistanceView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user = request.user
        serializer = PreferenceDistanceSerializer(user)
        jd = {'success' : True}
        jd.update(serializer.data)
        res = jd
        return response.Response(res)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     you = User_Preferences_Distance.objects.get(preference_distance_id=id)
        # except:
        #     res = {'success' : False, 'error' : "id does not exist"}
        #     return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        serializer=PreferenceDistanceSerializer(data=jd,partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : serializer.errors}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        res = {'success' : True, 'distance': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class PreferenceGloballyView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        res = {'success': True, 'search_globally': ''}
        return response.Response(res)

    def patch(self, request):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     you = User_Preferences_Globally.objects.get(preference_globally_id=id)
        # except:
        #     res = {'success' : False, 'error' : "id does not exist"}
        #     return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceGloballySerializer(data=jd,partial=True)
        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : serializer.errors}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
        res = {'success' : True, 'globally': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)


class PreferenceUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EditPreferenceSerializer

    def get(self, request):
        user = request.user
        res = {'success' : True, 'user': {}}
        return response.Response(res)

    def patch(self, request):
        jd = request.data
        #id = request.user.id
        context = {}
        # try:
        #     user_obj = User.objects.get(id=id)
        # except User.DoesNotExist:
        #     res = {'success' : False, 'error' : "User id does not exist."}
        #     return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        request_keys = list(jd.keys())
        allowed_keys = [e.value for e in User_Fields]
        for key in request_keys:
            if key not in allowed_keys:
                res = {'success' : False,
                        'error' : "Wrong parameter(s) passed in request."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

        for field in List_Fields:
            field_name = field.value

            if field_name in jd:
                field_list = jd[field_name]
                res = validate_field(field_name, field_list)
                if res:
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)
                context[field_name] = field_list

        serializer = EditPreferenceSerializer(user_obj, data=jd, context=context, partial=True)

        if serializer.is_valid():
            serializer.save()
            serialized_data = (serializer.data).copy()
            for field in serializer.data:
                if field not in jd and field != 'preference_gender_name':
                    serialized_data.pop(field)
            if 'preference_gender' in jd:
                serialized_data.pop('gender')
            if 'preference_gender' not in jd:
                serialized_data.pop('preference_gender_name')
            res = {'success' : True, 'user': serialized_data}
            return response.Response(res, status=status.HTTP_201_CREATED)
        res = {'success' : False, 'user': serializer.errors}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)
