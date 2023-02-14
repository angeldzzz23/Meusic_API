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


# registration tests

class LoginTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.client = Client()

	def test_login_with_existing_account_is_valid(self):
		response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(content["success"], True)

	def test_login_with_nonexistent_account_is_invalid(self):
		response = self.client.post('/api/auth/login', {'email': 'aaaaaa@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		content = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(content, {"success": False, "message": "invalid credentials, try again"})

class UserTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='testuser@gmail.com', password='password')
		self.client = Client()

		### APIFactory:
		# self.factory = APIRequestFactory()
		# self.factory_token = Token.objects.create(user=self.user)
		# self.factory_token.save()

		### APIClient:
		# self.client = APIClient()
		# client.login(email='testuser@gmail.com', password='password')

	def test_get_user_without_being_authenticated(self):
		login_response = self.client.post('/api/auth/login', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		response = self.client.get('/api/auth/user', {'email': 'testuser@gmail.com', 'password' : 'password'}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		content = json.loads(response.content)

		### If using force authentication and APIFactory
		#request = self.factory.get('/api/auth/user', HTTP_AUTHORIZATION='Token {}'.format(self.token))
		#force_authenticate(request, user=self.user)
		#view = AuthUserAPIView.as_view()
		# request_view = view(request)
		# content = json.loads(response.content)


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

class RegistrationTest(TestCase):
	def setUp(self):
		self.client = Client()

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