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



# def editUser():
# 	login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
# 	login_response_body = json.loads(login_response.content)
# 	token = login_response_body['access']  # Gets the token
# 	response = self.client.patch('/api/auth/user', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
# 	content = json.loads(response.content)

# 		data = {
#     			"success": True,
#     			"user": {}
# 				}

# 		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
# 		self.assertEqual(content, data)







class MatchesTests(TestCase):
	def setUp(self):
		# 1) Creating the user
		# 2) Filling the models
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.user = User.objects.create_user(email='david@gmail.com', password='pass')
		self.user = User.objects.create_user(email='gerardo@gmail.com', password='pass')
		self.user = User.objects.create_user(email='yorbin@gmail.com', password='pass')


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

		def editUsername(token, username):
			data = json.dumps({'username': username})
			response = self.client.patch('/api/auth/user', data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			return response.status_code

		def likeUser(token, message, username):
			data = message
			if data == None: 
				liking_user_response = self.client.post('/api/newsfeed/like/' + username, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
				return liking_user_response

			toJson = json.dumps({'message' : message})
			liking_user_response = self.client.post('/api/newsfeed/like/' + username, data=toJson,content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			return liking_user_response



		def logInSecondUser(email, password): 
			login_response_userone = self.client.post('/api/auth/login', {'email': email, 'password' : password}, HTTP_ACCEPT='application/json')
			login_response_body_userOne = json.loads(login_response_userone.content)
			tokenUserOne = login_response_body_userOne['access']  # Gets the token
			return tokenUserOne

		# editing the user 
		tokenUserOne = logInSecondUser('aa@gmail.com', 'pass')
		statusCode = editUsername(tokenUserOne, 'angelzzz23')
		# making sure that the editing of the user 1 was done correctly 
		self.assertEqual(201, statusCode)

		tokenUserTwo = logInSecondUser('david@gmail.com', 'pass')
		statusCode = editUsername(tokenUserTwo, 'davidzzz23')
		self.assertEqual(201, statusCode)

		tokenUserThree = logInSecondUser('gerardo@gmail.com', 'pass')
		statusCode = editUsername(tokenUserThree, 'gerardo24')
		self.assertEqual(201, statusCode)


		tokenUserFour = logInSecondUser('yorbin@gmail.com', 'pass')
		statusCode = editUsername(tokenUserFour, 'yorbinCastigador')
		self.assertEqual(201, statusCode)		

		# get the matches of the user with no matches 

		# log the user in 
		user_before_request = self.client.get('/api/matches/', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {tokenUserOne}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 


		# have user one like all three other users 
		user_before_request = self.client.get('/api/matches/', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {tokenUserOne}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		expected_data = {
    					"success": True,
    					"Matches": []
						}

		self.assertEqual(expected_data, user_before_request_content)	



		# like the user 
		like_user_two = likeUser(tokenUserOne, None, 'davidzzz23')
		like_user_two_expected_data = {'success': True, 'isMatch': False}

		self.assertEqual(like_user_two_expected_data,like_user_two.data)

		# this is testing for a match without a message 
		user_two_liking_user_one = likeUser(tokenUserTwo, None, 'angelzzz23')
		user_two_liking_user_one_expected_data = {'success': True, 'isMatch': True, 'user': {'username': 'angelzzz23', 'message': None}}
		
		self.assertEqual(user_two_liking_user_one_expected_data,user_two_liking_user_one.data)


		# user one liking usertwo 
		like_user_three = likeUser(tokenUserOne, 'liking the user', 'yorbinCastigador')
		liking_user_three_expected_Data = {'success': True, 'isMatch': False}
		self.assertEqual(liking_user_three_expected_Data,like_user_three.data)

		user_four_liking_user_one = likeUser(tokenUserFour, None, 'angelzzz23')
		expected_data_four_one= {'success': True, 'isMatch': True, 'user': {'username': 'angelzzz23', 'message': 'liking the user'}}
		self.assertEqual(expected_data_four_one, user_four_liking_user_one.data)



		# testing the user with all of their matches
		user_before_request = self.client.get('/api/matches/', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {tokenUserOne}'} )
		expected_data_for_user_data = {'success': True, 'Matches': [{'username': 'yorbinCastigador', 'first_name': None, 'last_name': None, 'feed_item_url': 'http://testserver/api/newsfeed/user/yorbinCastigador', 'video': None, 'message': 'liking the user', 'id': 2}, {'username': 'davidzzz23', 'first_name': None, 'last_name': None, 'feed_item_url': 'http://testserver/api/newsfeed/user/davidzzz23', 'video': None, 'message': None, 'id': 1}]}

		self.assertEqual(expected_data_for_user_data, user_before_request.data)



 




