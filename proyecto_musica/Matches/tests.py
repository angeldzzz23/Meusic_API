from django.test import TestCase
from authentication.models import User
from rest_framework.test import APIRequestFactory
from django.test import Client
import json
from django.test import TestCase, Client
from rest_framework import status 
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from authentication.views import AuthUserAPIView
from authentication.views import VerifyEmail
from authentication.models import Genders, Skills, Genres, Nationality


# from authentication.views import AuthUserAPIView, VerifyEmail
# from authentication.models import User, Genders, Skills, Genres
# from preferences.models import User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
# from django.core import mail



class MatchesTests(TestCase):
	def setUp(self):
		# 1) Creating the user
		# 2) Filling the models
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.client = Client()

		# Genders.objects.create(gender_id=1, gender_name="male")
		# Genders.objects.create(gender_id=2, gender_name="female")

		# Skills.objects.create(skill_id=1, skill_name="singing")
		# Skills.objects.create(skill_id=2, skill_name="dancing")
		# Skills.objects.create(skill_id=3, skill_name="cooking")
		# Skills.objects.create(skill_id=4, skill_name="driving")
		# Skills.objects.create(skill_id=5, skill_name="drawing")

		# Genres.objects.create(genre_id=1, genre_name="rap")
		# Genres.objects.create(genre_id=2, genre_name="R&B")
		# Genres.objects.create(genre_id=3, genre_name="pop")

	def test_user_matches(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		# log the user in 
		user_before_request = self.client.get('/api/matches/', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		print('test content', user_before_request_content)		

		# get the matches of the user with no matches 

		# getting the user matches with at least one match 




