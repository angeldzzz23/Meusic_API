from rest_framework.test import APIRequestFactory
import json
from django.test import TestCase, Client
from rest_framework import status 
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from authentication.views import AuthUserAPIView, VerifyEmail
from authentication.models import User, Genders, Skills, Genres
from preferences.models import User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
from django.core import mail



class PreferencesGendersTest(TestCase):
	def setUp(self):
		# 1) Creating the user
		# 2) Filling the models
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.client = Client()

		Genders.objects.create(gender_id=1, gender_name="male")
		Genders.objects.create(gender_id=2, gender_name="female")

		Skills.objects.create(skill_id=1, skill_name="singing")
		Skills.objects.create(skill_id=2, skill_name="dancing")
		Skills.objects.create(skill_id=3, skill_name="cooking")
		Skills.objects.create(skill_id=4, skill_name="driving")
		Skills.objects.create(skill_id=5, skill_name="drawing")

		Genres.objects.create(genre_id=1, genre_name="rap")
		Genres.objects.create(genre_id=2, genre_name="R&B")
		Genres.objects.create(genre_id=3, genre_name="pop")


	# Testing login into existing account
	def test_genders(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_genders = self.client.patch('/api/user/preferences/all', data=json.dumps({"genders": [1, 2]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_genders = json.loads(resp_genders.content)
		user_after_request_genders = self.client.get('/api/user/preferences/gender', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_genders = json.loads(user_after_request_genders.content)

		expected_data = {
    					"success": True,
    					"genders": [
        							"male",
        							"female"
    								]
						}

		self.assertEqual(expected_data, user_after_request_content_genders)

	def test_genders_not_in_a_list(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_genders = self.client.patch('/api/user/preferences/all', data=json.dumps({"genders": 1}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_genders = json.loads(resp_genders.content)

		expected_data = {
    					"success": False,
    					"error": "Field for genders should be in a list."
						}

		self.assertEqual(expected_data, resp_content_genders)

	def test_genders_not_existing_in_database(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_genders = self.client.patch('/api/user/preferences/all', data=json.dumps({"genders": [3]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_genders = json.loads(resp_genders.content)

		expected_data = {
    					"success": False,
    					"error": "Could not find one or several genders in database."
						}

		self.assertEqual(expected_data, resp_content_genders)

	def test_genders_with_a_string_in_list(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_genders = self.client.patch('/api/user/preferences/all', data=json.dumps({"genders": ["male"]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_genders = json.loads(resp_genders.content)

		expected_data = {
    					"success": False,
    					"error": "Please enter numeric genders."
						}

		self.assertEqual(expected_data, resp_content_genders)




class PreferencesSkillsTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.client = Client()

		Skills.objects.create(skill_id=1, skill_name="singing")
		Skills.objects.create(skill_id=2, skill_name="dancing")
		Skills.objects.create(skill_id=3, skill_name="cooking")
		Skills.objects.create(skill_id=4, skill_name="driving")
		Skills.objects.create(skill_id=5, skill_name="drawing")
		Skills.objects.create(skill_id=6, skill_name="football")

	def test_skills(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_skills = self.client.patch('/api/user/preferences/all', data=json.dumps({"skills": [1,2,3]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_skills = json.loads(resp_skills.content)
		user_after_request_skills = self.client.get('/api/user/preferences/skill', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_skills = json.loads(user_after_request_skills.content)

		expected_data = {
    					"success": True,
    					"skills": [
        						{
            					"skill_id": 1,
            					"skill_name": "singing"
        						},
        						{
            					"skill_id": 2,
            					"skill_name": "dancing"
        						},
        						{
            					"skill_id": 3,
            					"skill_name": "cooking"
        						}
    							]
						}

		self.assertEqual(expected_data, user_after_request_content_skills)

	def test_skills_not_in_a_list(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_skills = self.client.patch('/api/user/preferences/all', data=json.dumps({"skills": 2}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_skills = json.loads(resp_skills.content)

		expected_data = {
    					"success": False,
    					"error": "Field for skills should be in a list."
						}

		self.assertEqual(expected_data, resp_content_skills)

	def test_skills_not_in_database(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_skills = self.client.patch('/api/user/preferences/all', data=json.dumps({"skills": [7]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_skills = json.loads(resp_skills.content)

		expected_data = {
    					"success": False,
    					"error": "Could not find one or several skills in database."
						}

		self.assertEqual(expected_data, resp_content_skills)

	def test_no_more_than_5_skills_allowed(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_skills = self.client.patch('/api/user/preferences/all', data=json.dumps({"skills": [1,2,3,4,5,6]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_skills = json.loads(resp_skills.content)

		expected_data = {
    					"success": False,
    					"error": "Cannot submit more than 5 skills."
						}

		self.assertEqual(expected_data, resp_content_skills)


class PreferencesGenresTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.client = Client()

		Genres.objects.create(genre_id=1, genre_name="pop")
		Genres.objects.create(genre_id=2, genre_name="rap")
		Genres.objects.create(genre_id=3, genre_name="R&B")
		Genres.objects.create(genre_id=4, genre_name="rock")
		Genres.objects.create(genre_id=5, genre_name="country")
		Genres.objects.create(genre_id=6, genre_name="k-pop")

	def test_genres(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_genres = self.client.patch('/api/user/preferences/all', data=json.dumps({"genres": [1,4]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_genres = json.loads(resp_genres.content)
		user_after_request_genres = self.client.get('/api/user/preferences/genre', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_genres = json.loads(user_after_request_genres.content)

		expected_data = {
    					"success": True,
    					"genres": [
        							{
            						"genre_id": 1,
            						"genre_name": "pop"
        							},
        							{
            						"genre_id": 4,
            						"genre_name": "rock"
        							}
    							]
						}

		self.assertEqual(expected_data, user_after_request_content_genres)

	def test_genres_not_in_a_list(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_genres = self.client.patch('/api/user/preferences/all', data=json.dumps({"genres": 5}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_genres = json.loads(resp_genres.content)
		

		expected_data = {
    					"success": False,
    					"error": "Field for genres should be in a list."
						}

		self.assertEqual(expected_data, resp_content_genres)

	def test_genres_not_in_database(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_genres = self.client.patch('/api/user/preferences/all', data=json.dumps({"genres": [8]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_genres = json.loads(resp_genres.content)
		

		expected_data = {
    					"success": False,
    					"error": "Could not find one or several genres in database."
						}

		self.assertEqual(expected_data, resp_content_genres)

	def test_no_more_than_5_genres_allowed(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_genres = self.client.patch('/api/user/preferences/all', data=json.dumps({"genres": [1,2,3,4,5,6]}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_genres = json.loads(resp_genres.content)
		

		expected_data = {
    					"success": False,
    					"error": "Cannot submit more than 5 genres."
						}

		self.assertEqual(expected_data, resp_content_genres)


class PreferencesAgeTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.client = Client()


	def test_age(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_age = self.client.patch('/api/user/preferences/all', data=json.dumps({"age": {"low": 50, "high": 80}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_age = json.loads(resp_age.content)
		user_after_request_age = self.client.get('/api/user/preferences/age', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_age = json.loads(user_after_request_age.content)

		expected_data = {
    					"success": True,
    					"age": {
        						"low": 50,
       					 		"high": 80
    							}
						}

		self.assertEqual(expected_data, user_after_request_content_age)

	def test_age_is_missing_low(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_age = self.client.patch('/api/user/preferences/all', data=json.dumps({"age": {"gwg": 50, "high": 80}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_age = json.loads(resp_age.content)

		expected_data = {
    					"success": False,
    					"error": "low and high are the only allowed keys for age."
						}

		self.assertEqual(expected_data, resp_content_age)

	def test_age_is_missing_high(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_age = self.client.patch('/api/user/preferences/all', data=json.dumps({"age": {"low": 50, "lsnvls": 80}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_age = json.loads(resp_age.content)

		expected_data = {
    					"success": False,
    					"error": "low and high are the only allowed keys for age."
						}

		self.assertEqual(expected_data, resp_content_age)


	def test_age_low_greater_than_high(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_age = self.client.patch('/api/user/preferences/all', data=json.dumps({"age": {"low": 50, "high": 40}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_age = json.loads(resp_age.content)

		expected_data = {
			"success": False,
    		"error": "low must be <= high in age."
		}
		
		self.assertEqual(expected_data, resp_content_age)

	def test_age_contains_a_string_value_for_low(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_age = self.client.patch('/api/user/preferences/all', data=json.dumps({"age": {"low": "35", "high": 40}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_age = json.loads(resp_age.content)

		expected_data = {
    					"success": False,
    					"error": "Each value must be an integer in age."
						}
		
		self.assertEqual(expected_data, resp_content_age)

	def test_age_contains_a_string_value_for_high(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_age = self.client.patch('/api/user/preferences/all', data=json.dumps({"age": {"low": 50, "high": "55"}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_age = json.loads(resp_age.content)

		expected_data = {
    					"success": False,
    					"error": "Each value must be an integer in age."
						}
		
		self.assertEqual(expected_data, resp_content_age)



class PreferenceDistanceTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.client = Client()


	def test_distance(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_distance = self.client.patch('/api/user/preferences/all', data=json.dumps({"distance": {"low": 0, "high": 5}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_distance = json.loads(resp_distance.content)
		user_after_request_distance = self.client.get('/api/user/preferences/distance', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_distance = json.loads(user_after_request_distance.content)

		expected_data = {
    					"success": True,
    					"distance": {
        							"low": 0,
        							"high": 5
    								}
						}

		self.assertEqual(expected_data, user_after_request_content_distance)

	def test_distance_is_missing_low(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_distance = self.client.patch('/api/user/preferences/all', data=json.dumps({"distance": {"a": 0, "high": 5}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_distance = json.loads(resp_distance.content)

		expected_data = {
    					"success": False,
    					"error": "low and high are the only allowed keys for distance."
						}

		self.assertEqual(expected_data, resp_content_distance)

	def test_distance_is_missing_high(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_distance = self.client.patch('/api/user/preferences/all', data=json.dumps({"distance": {"low": 0, "lsdkvskd": 5}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_distance = json.loads(resp_distance.content)

		expected_data = {
    					"success": False,
    					"error": "low and high are the only allowed keys for distance."
						}

		self.assertEqual(expected_data, resp_content_distance)

	def test_distance_low_greater_than_high(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_distance = self.client.patch('/api/user/preferences/all', data=json.dumps({"distance": {"low": 50, "high": 40}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_distance = json.loads(resp_distance.content)

		expected_data = {
			"success": False,
    		"error": "low must be <= high in distance."
		}
		
		self.assertEqual(expected_data, resp_content_distance)

	def test_distance_contains_a_string_value_for_low(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_distance = self.client.patch('/api/user/preferences/all', data=json.dumps({"distance": {"low": "some_string", "high": 40}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_distance = json.loads(resp_distance.content)

		expected_data = {
    					"success": False,
    					"error": "Each value must be an integer in distance."
						}
		
		self.assertEqual(expected_data, resp_content_distance)

	def test_distance_contains_a_string_value_for_high(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_distance = self.client.patch('/api/user/preferences/all', data=json.dumps({"distance": {"low": 40, "high": "some_string"}}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_distance = json.loads(resp_distance.content)

		expected_data = {
    					"success": False,
    					"error": "Each value must be an integer in distance."
						}
		
		self.assertEqual(expected_data, resp_content_distance)



class PreferenceGloballyTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.client = Client()


	def test_globally(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		resp_globally = self.client.patch('/api/user/preferences/all', data=json.dumps({"search_globally": True}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_globally = json.loads(resp_globally.content)
		user_after_request_globally = self.client.get('/api/user/preferences/search_globally', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_globally = json.loads(user_after_request_globally.content)

		expected_data = {
    					"success": True,
    					"search_globally": True
						}

		self.assertEqual(expected_data, user_after_request_content_globally)

	def test_globally_not_boolean(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token
		user_before_request = self.client.get('/api/user/preferences/all', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_before_request_content = json.loads(user_before_request.content) # get the user preferences body before patch 

		first_patch = self.client.patch('/api/user/preferences/all', data=json.dumps({"search_globally": True}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		first_patch_get = self.client.get('/api/user/preferences/search_globally', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		first_patch_get_content = json.loads(first_patch_get.content)

		resp_globally = self.client.patch('/api/user/preferences/all', data=json.dumps({"search_globally": "some_string"}), content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		resp_content_globally = json.loads(resp_globally.content)
		user_after_request_globally = self.client.get('/api/user/preferences/search_globally', content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'} )
		user_after_request_content_globally = json.loads(user_after_request_globally.content)

		expected_data_1 = {
    					"success": False,
    					"error": "Field for search_globally should be a boolean."
						}
		expected_data_2 = {
    					"success": True,
    					"search_globally" : True
						}

		self.assertEqual(expected_data_1, resp_content_globally)
		self.assertEqual(expected_data_2, first_patch_get_content)