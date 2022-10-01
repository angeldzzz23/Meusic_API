from django.shortcuts import render
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView

# this gets the inbox of the user
class InboxView(GenericAPIView):

    def get(self, request):
        res = {'success' : True, 'user': 'serialized_data'}
        return response.Response(res)
