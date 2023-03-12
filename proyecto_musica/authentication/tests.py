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
from django.core import mail



class LoginTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.client = Client()

	# Testing login into existing account
	def test_login_with_existing_account_is_valid(self):
		response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(content["success"], True)

	# Testing login into non-existing account
	def test_login_with_nonexistent_account_is_invalid(self):
		response = self.client.post('/api/auth/login', {'email': 'aaaaaa@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(content, {"success": False, "message": "invalid credentials, try again"})

	# Testing for returned cookies in both COOKIES and JSON response
	def test_cookies_for_login(self):
		response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)

		assert content["success"] == True
		assert "access" in content
		assert "access" in response.client.cookies
		assert "refresh" in content
		assert "refresh_token" in response.client.cookies


class UserTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.client = Client()


	# Testing GET for user with token while being logged in
	def test_get_user_while_being_authenticated(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.get('/api/auth/user', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		data = {
			"success": True,
    		"user": {
        	"username": None,
        	"email": "testuser@gmail.com",
        	"first_name": None,
        	"last_name": None,
        	"gender_name": None,
        	"DOB": None,
        	"about_me": None,
        	"skills": None,
        	"genres": None,
        	"artists": None,
        	"pictures": None,
       		"video": None,
        	"videos": None,
        	"nationalities": None,
        	"location": None
   			}
		}

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(content, data) 

	# Testing PATCH for user with empty request body
	def test_patch_with_empty_body(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.patch('/api/auth/user', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		data = {
    			"success": True,
    			"user": {}
				}

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(content, data)

	# Testing PATCH for user without being authenticated
	def test_patch_without_being_authenticated(self):
		response = self.client.patch('/api/auth/user', HTTP_ACCEPT='application/json')
		content = json.loads(response.content)

		data = {
    			"detail": "Authentication credentials were not provided."
				}

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(content, data)


	# Testing DELETE for user -- response
	def test_logged_in_user_gets_deleted_successfully(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.delete('/api/auth/user', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		data = {
   		 		"success": True,
    			"message": "user has been deleted"
				}

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(content, data)

	# Testing DELETE for user -- user gets removed from the database
	def test_user_gets_deleted_successfully(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.delete('/api/auth/user', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)

		data = {
    			"success": False,
    			"message": "invalid credentials, try again"
				}

		self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(login_response_body, data)

	# Testing DELETE for not logged in user
	def test_not_logged_in_user_deletion(self):
		response = self.client.delete('/api/auth/user', HTTP_ACCEPT='application/json')
		content = json.loads(response.content)

		data = {
    			"detail": "Authentication credentials were not provided."
				}

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(content, data)


	# Testing PATCH for the user with invalid parameter passed in the request body
	def test_patch_with_invalid_parameter(self): 							
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		#response = self.client.patch('/api/auth/user', data={"usernam" : "danil"}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		#content = json.loads(response.content)

		resp = self.client.patch('/api/auth/user', data=json.dumps({"name" : "123"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		content = json.loads(resp.content)

		data = {
    			"success": False,
    			"error": "Wrong parameter(s) passed in request."
				}

		#self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(content, data)
		self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)


	# Testing that the username has to be unique
	def test_username_must_be_unique(self):
		self.user = User.objects.create_user(email='testusersecond@gmail.com', password='password')

		login_response_first = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body_first = json.loads(login_response_first.content)
		token_first = login_response_body_first['access']  # Gets the token
		

		login_response_second = self.client.post('/api/auth/login', {'email': 'testusersecond@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body_second = json.loads(login_response_second.content)
		token_second = login_response_body_second['access']  # Gets the token

		response_one = self.client.patch('/api/auth/user', data=json.dumps({"username" : "my_username"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token_first}'} )
		response_two = self.client.patch('/api/auth/user', data=json.dumps({"username" : "my_username"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token_second}'} )

		expected_response = {
    						"success": False,
    						"user": {
        							"username": [ "This field must be unique." ]
        							}
        					}

		self.assertEqual(expected_response, json.loads(response_two.content))
		self.assertEqual(response_two.status_code, status.HTTP_400_BAD_REQUEST)


	# Testing PATCH for every attribute, one by one
	def test_patch_every_attribute_of_user(self):
		Genders.objects.create(gender_id=1, gender_name="male")

		Skills.objects.create(skill_id=1, skill_name="singing")
		Skills.objects.create(skill_id=2, skill_name="dancing")
		Skills.objects.create(skill_id=3, skill_name="cooking")
		Skills.objects.create(skill_id=4, skill_name="driving")
		Skills.objects.create(skill_id=5, skill_name="drawing")

		Genres.objects.create(genre_id=1, genre_name="rap")
		Genres.objects.create(genre_id=2, genre_name="R&B")
		Genres.objects.create(genre_id=3, genre_name="pop")

		Nationality.objects.create(nationality_id=1, nationality_name="russian")
		Nationality.objects.create(nationality_id=2, nationality_name="american")
		Nationality.objects.create(nationality_id=3, nationality_name="canadian")


		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content)

		resp_username = self.client.patch('/api/auth/user', data=json.dumps({"username" : "test_username"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_username = json.loads(resp_username.content)
		user_after_request_username = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_username = json.loads(user_after_request_username.content)

		# PATCH username
		expected_before_request_username = {
    						"success": True,
    						"user": {
        							"username": None,
        							"email": "testuser@gmail.com",
        							"first_name": None,
        							"last_name": None,
        							"gender_name": None,
        							"DOB": None,
        							"about_me": None,
        							"skills": None,
        							"genres": None,
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}

		expected_after_request_username = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": None,
        							"last_name": None,
        							"gender_name": None,
        							"DOB": None,
        							"about_me": None,
        							"skills": None,
        							"genres": None,
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}
		expected_response_username = {
    						"success": True,
    						"user": {
        							"username": "test_username"
    								}
							}

		# PATCH first_name
		resp = self.client.patch('/api/auth/user', data=json.dumps({"first_name" : "Danil"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_first_name= json.loads(resp.content)
		user_after_request_first_name = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_first_name = json.loads(user_after_request_first_name.content)

		expected_after_request_first_name = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": None,
        							"gender_name": None,
        							"DOB": None,
        							"about_me": None,
        							"skills": None,
        							"genres": None,
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}
		expected_response_first_name = {
    						"success": True,
    						"user": {
        							"first_name": "Danil"
    								}
							}

		# PATCH last_name
		resp = self.client.patch('/api/auth/user', data=json.dumps({"last_name" : "Merinov"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_last_name= json.loads(resp.content)
		user_after_request_last_name = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_last_name = json.loads(user_after_request_last_name.content)

		expected_after_request_last_name = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": None,
        							"DOB": None,
        							"about_me": None,
        							"skills": None,
        							"genres": None,
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}
		expected_response_last_name = {
    						"success": True,
    						"user": {
        							"last_name": "Merinov"
    								}
							}

		# PATCH gender_name
		resp = self.client.patch('/api/auth/user', data=json.dumps({"gender" : 1}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_gender= json.loads(resp.content)
		user_after_request_gender = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_gender = json.loads(user_after_request_gender.content)

		expected_after_request_gender = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": "male",
        							"DOB": None,
        							"about_me": None,
        							"skills": None,
        							"genres": None,
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}
		expected_response_gender = {
    						"success": True,
    						"user": {
        							"gender_name": "male"
    								}
							}

		# PATCH DOB
		resp = self.client.patch('/api/auth/user', data=json.dumps({"DOB" : "2001-11-22"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_DOB= json.loads(resp.content)
		user_after_request_DOB = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_DOB = json.loads(user_after_request_DOB.content)

		expected_after_request_DOB = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": "male",
        							"DOB": "2001-11-22",
        							"about_me": None,
        							"skills": None,
        							"genres": None,
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}

		expected_response_DOB = {
    							"success": True,
    							"user": {
        								"DOB": "2001-11-22"
    									}
								}

		# PATCH about_me
		resp = self.client.patch('/api/auth/user', data=json.dumps({"about_me" : "I love hockey, soccer, and currently live in Philadelphia"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_about_me= json.loads(resp.content)
		user_after_request_about_me = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_about_me = json.loads(user_after_request_about_me.content)

		expected_after_request_about_me = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": "male",
        							"DOB": "2001-11-22",
        							"about_me": "I love hockey, soccer, and currently live in Philadelphia",
        							"skills": None,
        							"genres": None,
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}

		expected_response_about_me = {
    							"success": True,
    							"user": {
        								"about_me": "I love hockey, soccer, and currently live in Philadelphia"
    									}
								}

		# PATCH skills
		resp = self.client.patch('/api/auth/user', data=json.dumps({"skills" : [1, 3, 5]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_skills= json.loads(resp.content)
		user_after_request_skills = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_skills = json.loads(user_after_request_skills.content)

		expected_after_request_skills = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": "male",
        							"DOB": "2001-11-22",
        							"about_me": "I love hockey, soccer, and currently live in Philadelphia",
        							"skills": [
            									{
                								"skill_id": 1,
               				 					"skill_name": "singing"
            									},
            									{
                								"skill_id": 3,
                								"skill_name": "cooking"
            									},
           			 							{
                								"skill_id": 5,
                								"skill_name": "drawing"
            									}
        									],
        							"genres": None,
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}

		expected_response_skills = {
    								"success": True,
    								"user": {
        									"skills": [
            											{
                										"skill_id": 1,
                										"skill_name": "singing"
            											},
            											{
                										"skill_id": 3,
                										"skill_name": "cooking"
            											},
            											{
                										"skill_id": 5,
                										"skill_name": "drawing"
            											}
        											]
    										}
									}

		# PATCH genres
		resp = self.client.patch('/api/auth/user', data=json.dumps({"genres" : [1, 2]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_genres= json.loads(resp.content)
		user_after_request_genres = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_genres = json.loads(user_after_request_genres.content)

		expected_after_request_genres = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": "male",
        							"DOB": "2001-11-22",
        							"about_me": "I love hockey, soccer, and currently live in Philadelphia",
        							"skills": [
            									{
                								"skill_id": 1,
               				 					"skill_name": "singing"
            									},
            									{
                								"skill_id": 3,
                								"skill_name": "cooking"
            									},
           			 							{
                								"skill_id": 5,
                								"skill_name": "drawing"
            									}
        									],
        							"genres": [
            									{
                								"genre_id": 1,
                								"genre_name": "rap"
            									},
            									{
                								"genre_id": 2,
                								"genre_name": "R&B"
            									}
        									],
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": None,
        							"location": None
    								}
								}

		expected_response_genres = {
    								"success": True,
    								"user": {
        									"genres": [
            										{
                									"genre_id": 1,
                									"genre_name": "rap"
            										},
            										{
                									"genre_id": 2,
                									"genre_name": "R&B"
            										}
        												]
    										}
									}

		# PATCH nationalities
		resp = self.client.patch('/api/auth/user', data=json.dumps({"nationalities" : [1, 2]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_nationality= json.loads(resp.content)
		user_after_request_nationality = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_nationality = json.loads(user_after_request_nationality.content)

		expected_after_request_nationality = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": "male",
        							"DOB": "2001-11-22",
        							"about_me": "I love hockey, soccer, and currently live in Philadelphia",
        							"skills": [
            									{
                								"skill_id": 1,
               				 					"skill_name": "singing"
            									},
            									{
                								"skill_id": 3,
                								"skill_name": "cooking"
            									},
           			 							{
                								"skill_id": 5,
                								"skill_name": "drawing"
            									}
        									],
        							"genres": [
            									{
                								"genre_id": 1,
                								"genre_name": "rap"
            									},
            									{
                								"genre_id": 2,
                								"genre_name": "R&B"
            									}
        									],
        							"artists": None,
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": [
            										{
                									"nationality_id": 1,
                									"nationality_name": "russian"
            										},
            										{
                									"nationality_id": 2,
                									"nationality_name": "american"
            										}
        												],
        							"location": None
    								}
								}

		expected_response_nationality = {
    								"success": True,
    								"user": {
        									"nationalities": [
            										{
                									"nationality_id": 1,
                									"nationality_name": "russian"
            										},
            										{
                									"nationality_id": 2,
                									"nationality_name": "american"
            										}
        												]
    										}
									}

		# PATCH artists
		resp = self.client.patch('/api/auth/user', data=json.dumps({"artists" : ["drake", "kanye"]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_artists= json.loads(resp.content)
		user_after_request_artists = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_artists = json.loads(user_after_request_artists.content)

		expected_after_request_artists = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": "male",
        							"DOB": "2001-11-22",
        							"about_me": "I love hockey, soccer, and currently live in Philadelphia",
        							"skills": [
            									{
                								"skill_id": 1,
               				 					"skill_name": "singing"
            									},
            									{
                								"skill_id": 3,
                								"skill_name": "cooking"
            									},
           			 							{
                								"skill_id": 5,
                								"skill_name": "drawing"
            									}
        									],
        							"genres": [
            									{
                								"genre_id": 1,
                								"genre_name": "rap"
            									},
            									{
                								"genre_id": 2,
                								"genre_name": "R&B"
            									}
        									],
        							"artists": [
            											{
                										"user_artist_id": 1,
                										"artist": "drake"
            											},
            											{
                										"user_artist_id": 2,
                										"artist": "kanye"
            											}
        												],
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": [
            										{
                									"nationality_id": 1,
                									"nationality_name": "russian"
            										},
            										{
                									"nationality_id": 2,
                									"nationality_name": "american"
            										}
        												],
        							"location": None
    								}
								}

		expected_response_artists = {
    								"success": True,
    								"user": {
        									"artists": [
            											{
                										"user_artist_id": 1,
                										"artist": "drake"
            											},
            											{
                										"user_artist_id": 2,
                										"artist": "kanye"
            											}
        												]
        												
    										}
									}

		# PATCH location
		resp = self.client.patch('/api/auth/user', data=json.dumps({"location" : {"lat": 11.2220, "long": 12.000}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_location= json.loads(resp.content)
		user_after_request_location = self.client.get('/api/auth/user', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_location = json.loads(user_after_request_location.content)

		expected_after_request_location = {
    						"success": True,
    						"user": {
        							"username": "test_username",
        							"email": "testuser@gmail.com",
        							"first_name": "Danil",
        							"last_name": "Merinov",
        							"gender_name": "male",
        							"DOB": "2001-11-22",
        							"about_me": "I love hockey, soccer, and currently live in Philadelphia",
        							"skills": [
            									{
                								"skill_id": 1,
               				 					"skill_name": "singing"
            									},
            									{
                								"skill_id": 3,
                								"skill_name": "cooking"
            									},
           			 							{
                								"skill_id": 5,
                								"skill_name": "drawing"
            									}
        									],
        							"genres": [
            									{
                								"genre_id": 1,
                								"genre_name": "rap"
            									},
            									{
                								"genre_id": 2,
                								"genre_name": "R&B"
            									}
        									],
        							"artists": [
            											{
                										"user_artist_id": 1,
                										"artist": "drake"
            											},
            											{
                										"user_artist_id": 2,
                										"artist": "kanye"
            											}
        												],
        							"pictures": None,
        							"video": None,
        							"videos": None,
        							"nationalities": [
            										{
                									"nationality_id": 1,
                									"nationality_name": "russian"
            										},
            										{
                									"nationality_id": 2,
                									"nationality_name": "american"
            										}
        												],
        							"location": {
            									"lat": 11.222,
            									"long": 12.0
        										}
    								}
								}

		expected_response_location = {
    								"success": True,
    								"user": {
        									"location": {
            											"lat": 11.222,
            											"long": 12.0
        												}
    										}

									}






		self.assertEqual(expected_before_request_username, user_before_request_content)
		self.assertEqual(expected_after_request_username, user_after_request_content_username)
		self.assertEqual(expected_response_username, resp_content_username)

		self.assertEqual(expected_after_request_first_name, user_after_request_content_first_name)
		self.assertEqual(expected_response_first_name, resp_first_name)

		self.assertEqual(expected_after_request_last_name, user_after_request_content_last_name)
		self.assertEqual(expected_response_last_name, resp_last_name)

		self.assertEqual(expected_after_request_gender, user_after_request_content_gender)
		self.assertEqual(expected_response_gender, resp_gender)

		self.assertEqual(expected_after_request_DOB, user_after_request_content_DOB)
		self.assertEqual(expected_response_DOB, resp_DOB)

		self.assertEqual(expected_after_request_about_me, user_after_request_content_about_me)
		self.assertEqual(expected_response_about_me, resp_about_me)

		self.assertEqual(expected_after_request_skills, user_after_request_content_skills)
		self.assertEqual(expected_response_skills, resp_skills)

		self.assertEqual(expected_after_request_genres, user_after_request_content_genres)
		self.assertEqual(expected_response_genres, resp_genres)

		self.assertEqual(expected_after_request_nationality, user_after_request_content_nationality)
		self.assertEqual(expected_response_nationality, resp_nationality)

		self.assertEqual(expected_after_request_artists, user_after_request_content_artists)
		self.assertEqual(expected_response_artists, resp_artists)

		self.assertEqual(expected_after_request_location, user_after_request_content_location)
		self.assertEqual(expected_response_location, resp_location)




class RegistrationTest(TestCase):
	def setUp(self):
		self.client = Client()


	# Testing registration without password provided in the request
	def test_password_is_missing(self):
		login_response = self.client.post('/api/auth/register', {'email': 'testuser@gmail.com'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		expected_response = {
    					"success": False,
    					"user": {
        						"password": [ "This field is required." ]
    							}
					}
		self.assertEqual(expected_response, login_response_body)
		self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)

	# Testing registration with invalid password of less than 6 characters long
	def test_registration_with_password_less_than_6_characters_is_invalid(self):
		login_response = self.client.post('/api/auth/register', {'email': 'testuser@gmail.com', 'password' : '123'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		expected_response = {
    				"success": False,
    				"user": {
        					"password": [ "Ensure this field has at least 6 characters." ]
    						}
					}
		self.assertEqual(expected_response, login_response_body)
		self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)


	# Testing registration with valid password of 6 characters long
	def test_registration_with_password_exactly_6_characters_is_valid(self):
		login_response = self.client.post('/api/auth/register', {'email': 'testuser@gmail.com', 'password' : '123456'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		expected_response = {
    		"success": True,
    		"user": {
        	"username": None,
        	"email": "testuser@gmail.com",
        	"first_name": None,
        	"last_name": None,
       		"gender_name": None,
       		"DOB": None,
        	"about_me": None,
        	"skills": None,
        	"genres": None,
        	"artists": None,
        	"pictures": None,
        	"video": None,
        	"videos": None,
        	"nationalities": None,
        	"location": None
    		}
		}
		self.assertEqual(expected_response, login_response_body)
		self.assertEqual(login_response.status_code, status.HTTP_201_CREATED)

	# Testing registration with valid password of more than 6 characters long
	def test_registration_with_password_emore_than_6_characters_is_valid(self):
		login_response = self.client.post('/api/auth/register', {'email': 'testuser@gmail.com', 'password' : '1234567'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		expected_response = {
    		"success": True,
    		"user": {
        	"username": None,
        	"email": "testuser@gmail.com",
        	"first_name": None,
        	"last_name": None,
       		"gender_name": None,
       		"DOB": None,
        	"about_me": None,
        	"skills": None,
        	"genres": None,
        	"artists": None,
        	"pictures": None,
        	"video": None,
        	"videos": None,
        	"nationalities": None,
        	"location": None
    		}
		}
		self.assertEqual(expected_response, login_response_body)
		self.assertEqual(login_response.status_code, status.HTTP_201_CREATED)

	# Testing registration with no email provided
	def test_registration_with_no_email_provided_is_invalid(self):
		login_response = self.client.post('/api/auth/register', {'password' : '1234567'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		expected_response = {
    						"success": False,
   							"user": {
        							"email": [ "This field is required." ]
    								}
							}


		self.assertEqual(expected_response, login_response_body)
		self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)

	# Testing registration with no email and password provided
	def test_registration_with_no_email_and_password_provided_is_invalid(self):
		login_response = self.client.post('/api/auth/register', {}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		expected_response = {
							"success": False,
							"user": {
									"email": [ "This field is required." ],
									"password": [ "This field is required." ]
        							}
        					}
		self.assertEqual(expected_response, login_response_body)
		self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)


class VerifyEmailTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.client = Client()


	# Testing POST for verifyemail when valid email is provided in the request body
	def test_post_verify_email_with_valid_email_provided(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.post('/api/auth/verifyemail/', {"email" : "aaa@gmail.com"}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		data = {
    			"success": True,
    			"message": "confirmation code was sent"
				}


		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(data, content)

	# Testing POST for verifyemail when invalid email is provided in the request body
	def test_post_verify_email_with_invalid_email_provided(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.post('/api/auth/verifyemail/', {"email" : "invalid_email"}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		data = {
    			"Success": False,
    			"Message": "Please enter a valid email address."
				}


		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(data, content)



	# Testing POST for verifyemail with no email provided in the request body
	def test_post_verify_email_with_email_not_provided(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.post('/api/auth/verifyemail/', {}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		data = {
    			"Success": False,
    			"Message": "Please include a verification email"
				}


		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(data, content)


	# Testing GET for verifyemail -- returns HTTP 400
	def test_get_verify_email(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.get('/api/auth/verifyemail/', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		data = {
    			"codigo": "400",
    			"message": "a message"
				}


		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(data, content)



class ForgotPasswordTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.client = Client()

	def test_forgotpassword_empty_request(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.post('/api/auth/forgotpassword/', {}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		data = {
    			"success": False,
    			"error": "no email"
				}


		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(data, content)

	def test_forgotpassword_with_provided_registered_email(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.post('/api/auth/forgotpassword/', {"email" : "testuser@gmail.com"}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)


		data = {
    			"success": True,
    			"message": "code has been sent"
				}

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(data, content)

	def test_forgotpassword_with_provided_unregistered_email(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.post('/api/auth/forgotpassword/', {"email" : "example@gmail.com"}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)


		data = {
    			"success": False,
    			"error": "not a valid user"
				}

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(data, content)


class VerifyForgotPassword(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.user = User.objects.create_user(email='danilmerinov9@gmail.com', password='password')
		self.client = Client()

	def test_get_verifyforgotpassword(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.get('/api/auth/forgotpassword/verify', {}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)


		data = {
    			"success": True,
    			"message": "wowowowowowoowowowowow"
				}

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(data, content)

	# def test_post_verifyforgotpassword_no_email_and_code(self):		Email verification not allowed
	# 	login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
	# 	login_response_body = json.loads(login_response.content)
	# 	token = login_response_body['access']  # Gets the token
	# 	response = self.client.patch('/api/auth/forgotpassword/verify', {"dsfd":"sdncksd"}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
	# 	content = json.loads(response.content)


	# 	data = {
    # 			"Success": False,
    # 			"Message": "Please verify presence of email and code"
	# 			}

	# 	self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	# 	self.assertEqual(data, content)

	# def test_post_verifyforgotpassword_invalid_token(self):		Email verification not allowed
	# 	login_response = self.client.post('/api/auth/login', {'email': 'danilmerinov9@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
	# 	login_response_body = json.loads(login_response.content)
	# 	token = login_response_body['access']  # Gets the token
	# 	response = self.client.patch('/api/auth/forgotpassword/verify', {"email":"danilmerinov9@gmail.com", "code": 435234}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
	# 	content = json.loads(response.content)


	# 	data = {
   	# 			"success": False,
    # 			"message": "invalid token"
	# 			}

	# 	self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	# 	self.assertEqual(data, content)
		



class refreshTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.user = User.objects.create_user(email='danilmerinov9@gmail.com', password='password')
		self.client = Client()

	def test_nothing_provided_in_the_body(self):
		response = self.client.post('/api/auth/refresh', {}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)


		data = {
    			"detail": "No valid token found in body 'refresh'",
    			"code": "token_not_valid"
				}

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(data, content)

	def test_cookies_refresh(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		refresh_token = login_response_body['refresh']  # Gets the token

		response = self.client.post('/api/auth/refresh', {"refresh" : refresh_token}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		assert "access" in content
		assert "refresh" in content
		assert "access" in response.client.cookies
		assert "refresh_token" in response.client.cookies


class refreshWCTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.client = Client()

	def test_cookies(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		response = self.client.post('/api/auth/refreshWC', {}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		assert "access" in content
		assert "refresh" in content
		assert "access" in response.client.cookies
		assert "refresh_token" in response.client.cookies

class VerifyEmailTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.client = Client()

	def test_get_verify_email(self):
		#login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		#login_response_body = json.loads(login_response.content)
		#refresh_token = login_response_body['refresh']  # Gets the token

		response = self.client.get('/api/auth/verifyemail/', HTTP_ACCEPT='application/json')
		content = json.loads(response.content)

		data = {
    		"codigo": "400",
    		"message": "a message"
			}
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(content, data)

	def test_existing_email_is_invalid(self):
		response = self.client.post('/api/auth/verifyemail/', {'email': 'testuser@gmail.com'}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)

		data = {
    			"success": False,
    			"message": "an account with that email already exists"
				}
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(content, data)



	def test_send_email(self):
		response = self.client.post('/api/auth/verifyemail/', {'email': 'example@gmail.com'})
		response_body = json.loads(response.content)

		self.assertEqual(len(mail.outbox), 1)

		email = mail.outbox[0]
		verification_code = email.body.split('\n')[-1]
		self.assertEqual(email.subject, 'Verify your email')
		self.assertTrue('Hi, this is your confirmation code. It expires in 5 minutes' in email.body)
		self.assertEqual(len(verification_code), 6)



