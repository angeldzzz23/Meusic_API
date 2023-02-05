from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from rest_framework import response
from authentication.models import User



class MatchesView(GenericAPIView):
    # this will get all of the matches
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        CurrentUser = request.user



        res = {'success' : True, 'hello ': 'world'}

        return response.Response(res, status=status.HTTP_200_OK)


class UnMatchView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):

        res = {'success' : True, 'isMatch ': False, 'user': {}}

        return response.Response(res, status=status.HTTP_201_CREATED)
