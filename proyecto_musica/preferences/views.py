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


from preferences.models import Preference_Genders, Preference_Skills, Preference_Genres


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



    def patch(self, request, id):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        try:
            you = Preference_Genders.objects.get(preference_gender_id=id)

        except:
            res = {'success' : False, 'error' : "id does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceGendersSerializer(you,data=jd,partial=True)

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
        # TODO: Add super user code

        # for testing pusposes I have it distabled
        user = request.user
        serializer = AllPreferenceSkillsSerializer(user)

        jd = {'success' : True}
        jd.update(serializer.data)

        res = jd
        return response.Response(res)


    def patch(self, request, id):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        try:
            you = Preference_Skills.objects.get(preference_skill_id=id)

        except:
            res = {'success' : False, 'error' : "id does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceSkillsSerializer(you,data=jd,partial=True)

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


    def patch(self, request, id):
        jd = request.data
        if request.user.is_superuser != True:
            res = {'success' : False, 'error' : "You do not have access to edit objs"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        try:
            you = Preference_Genres.objects.get(preference_genre_id=id)

        except:
            res = {'success' : False, 'error' : "id does not exist"}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer=PreferenceGenresSerializer(you,data=jd,partial=True)

        if serializer.is_valid():
            serializer.save()
        else:
            res = {'success' : False, 'error' : serializer.errors}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        res = {'success' : True, 'genre': serializer.data}
        return response.Response(res, status=status.HTTP_201_CREATED)



# class PreferenceAgeView(GenericAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     def get(self, request):
#         user = request.user
#         serializer = PreferenceAgeSerializer(user)
#         jd = {'success' : True}
#         jd.update(serializer.data)
#         res = jd
#         return response.Response(res)



# class PreferenceDistanceView(GenericAPIView):
# 	permission_classes = (permissions.IsAuthenticated,)
# 	def get(self, request):
# 		res = {'distance': {}}
# 		return response.Response(res)


# class PreferenceGloballyView(GenericAPIView):
# 	permission_classes = (permissions.IsAuthenticated,)
# 	def get(self, request):
# 		res = {'success': True, 'search_globally': ''}
# 		return response.Response(res)
