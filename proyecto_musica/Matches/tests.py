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



class MatchesTests(TestCase):
	def setUp(self):
		# 1) Creating the user
		# 2) Filling the models
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.user = User.objects.create_user(email='david@gmail.com', password='pass')
		self.user = User.objects.create_user(email='gerardo@gmail.com', password='pass')
		self.user = User.objects.create_user(email='yorbin@gmail.com', password='pass')


		self.client = Client()

	# helper method to log in the user 
	def logInSecondUser(self, email, password): 
		login_response_userone = self.client.post('/api/auth/login', {'email': email, 'password' : password}, HTTP_ACCEPT='application/json')
		login_response_body_userOne = json.loads(login_response_userone.content)
		tokenUserOne = login_response_body_userOne['access']  # Gets the token
		return tokenUserOne

	def editUsername(self, token, username):
		data = json.dumps({'username': username})
		response = self.client.patch('/api/auth/user', data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		return response.status_code

	def unmatching(self,token, username):
		response_unmatching_user = self.client.post('/api/matches/unmatch/' + username, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		return response_unmatching_user

	def likeUser(self, token, message, username):
			data = message
			if data == None: 
				liking_user_response = self.client.post('/api/newsfeed/like/' + username, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
				return liking_user_response

			toJson = json.dumps({'message' : message})
			liking_user_response = self.client.post('/api/newsfeed/like/' + username, data=toJson,content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			return liking_user_response


	def test_user_matches(self):
		# editing the user 
		tokenUserOne = self.logInSecondUser('aa@gmail.com', 'pass')
		statusCode = self.editUsername(tokenUserOne, 'angelzzz23')
		# making sure that the editing of the user 1 was done correctly 
		self.assertEqual(201, statusCode)

		tokenUserTwo = self.logInSecondUser('david@gmail.com', 'pass')
		statusCode = self.editUsername(tokenUserTwo, 'davidzzz23')
		self.assertEqual(201, statusCode)

		tokenUserThree = self.logInSecondUser('gerardo@gmail.com', 'pass')
		statusCode = self.editUsername(tokenUserThree, 'gerardo24')
		self.assertEqual(201, statusCode)


		tokenUserFour = self.logInSecondUser('yorbin@gmail.com', 'pass')
		statusCode = self.editUsername(tokenUserFour, 'yorbinCastigador')
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
		like_user_two = self.likeUser(tokenUserOne, None, 'davidzzz23')
		like_user_two_expected_data = {'success': True, 'isMatch': False}

		self.assertEqual(like_user_two_expected_data,like_user_two.data)

		# this is testing for a match without a message 
		user_two_liking_user_one = self.likeUser(tokenUserTwo, None, 'angelzzz23')
		user_two_liking_user_one_expected_data = {'success': True, 'isMatch': True, 'user': {'username': 'angelzzz23', 'message': None}}
		
		self.assertEqual(user_two_liking_user_one_expected_data,user_two_liking_user_one.data)


		# user one liking usertwo 
		like_user_three = self.likeUser(tokenUserOne, 'liking the user', 'yorbinCastigador')
		liking_user_three_expected_Data = {'success': True, 'isMatch': False}
		self.assertEqual(liking_user_three_expected_Data,like_user_three.data)

		user_four_liking_user_one = self.likeUser(tokenUserFour, None, 'angelzzz23')
		expected_data_four_one= {'success': True, 'isMatch': True, 'user': {'username': 'angelzzz23', 'message': 'liking the user'}}
		self.assertEqual(expected_data_four_one, user_four_liking_user_one.data)



		# testing the user with all of their matches
		user_before_request = self.client.get('/api/matches/', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {tokenUserOne}'} )




		expected_data_for_user_data = {'success': True, 'Matches': [{'username': 'yorbinCastigador', 'first_name': None, 'last_name': None, 'feed_item_url': 'http://testserver/api/newsfeed/user/yorbinCastigador', 'video': None, 'message': 'liking the user', 'id': 3}, {'username': 'davidzzz23', 'first_name': None, 'last_name': None, 'feed_item_url': 'http://testserver/api/newsfeed/user/davidzzz23', 'video': None, 'message': None, 'id': 2}]}
		self.assertEqual(expected_data_for_user_data, user_before_request.data)


	def test_unmatching(self):
		tokenUserOne = self.logInSecondUser('aa@gmail.com', 'pass')
		user_before_request = self.client.get('/api/matches/', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {tokenUserOne}'} )
		statusCode = self.editUsername(tokenUserOne, 'angelzzz23')
		# # making sure that the editing of the user 1 was done correctly 
		self.assertEqual(201, statusCode)

		tokenUserTwo = self.logInSecondUser('david@gmail.com', 'pass')
		statusCode = self.editUsername(tokenUserTwo, 'davidzzz23')
		self.assertEqual(201, statusCode)

		tokenUserThree = self.logInSecondUser('gerardo@gmail.com', 'pass')
		statusCode = self.editUsername(tokenUserThree, 'gerardo24')
		self.assertEqual(201, statusCode)



		# # like the user 
		like_user_two = self.likeUser(tokenUserOne, None, 'gerardo24')

		# # this is testing for a match without a message 
		user_two_liking_user_one = self.likeUser(tokenUserThree, None, 'angelzzz23')

		# checking the like 
		user_before_request = self.client.get('/api/matches/', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {tokenUserOne}'} )
		self.assertEqual(1, len(user_before_request.data['Matches']))

		# making sure the dislike button works
		response_after_unmatching = self.unmatching(tokenUserOne, 'gerardo24')
		# response_after_unmatching.refresh_from_db()
		# self.assertEqual(201, response_after_unmatching.status_code)

		# making sure that the unmatching worked 
		user_before_request2 = self.client.get('/api/matches/', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {tokenUserOne}'} )
		self.assertEqual(0, len(user_before_request2.data['Matches']))





