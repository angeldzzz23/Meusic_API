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
        	"youtube_vids": None,
        	"vimeo_vids": None,
        	"nationalities": None
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
        							"youtube_vids": None,
        							"vimeo_vids": None,
        							"nationalities": None
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
        							"youtube_vids": None,
        							"vimeo_vids": None,
        							"nationalities": None
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
        							"youtube_vids": None,
        							"vimeo_vids": None,
        							"nationalities": None
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
        							"youtube_vids": None,
        							"vimeo_vids": None,
        							"nationalities": None
    								}
								}
		expected_response_last_name = {
    						"success": True,
    						"user": {
        							"last_name": "Merinov"
    								}
							}




		self.assertEqual(expected_before_request_username, user_before_request_content)
		self.assertEqual(expected_after_request_username, user_after_request_content_username)
		self.assertEqual(expected_response_username, resp_content_username)

		self.assertEqual(expected_after_request_first_name, user_after_request_content_first_name)
		self.assertEqual(expected_response_first_name, resp_first_name)

		self.assertEqual(expected_after_request_last_name, user_after_request_content_last_name)
		self.assertEqual(expected_response_last_name, resp_last_name)



		
		

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
        	"youtube_vids": None,
        	"vimeo_vids": None,
        	"nationalities": None
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
        	"youtube_vids": None,
        	"vimeo_vids": None,
        	"nationalities": None
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


# ForgotPassword, VerifyForgotPassword, refreshWC, refresh






