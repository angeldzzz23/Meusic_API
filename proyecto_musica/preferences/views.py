from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions

class Gender(GenericAPIView):
	def get(self, request):
		res = {'success' : True, 'gender': {}}
		return response.Response(res)