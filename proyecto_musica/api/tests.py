from rest_framework.test import APIRequestFactory
import json
from django.test import TestCase, Client
from rest_framework import status 
from rest_framework.test import APITestCase, APIClient, force_authenticate
from rest_framework.authtoken.models import Token
from authentication.views import AuthUserAPIView, VerifyEmail
from authentication.models import User, Genders, Skills, Genres
from api.models import Images, Videos
from preferences.models import User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
from django.core import mail
import os
import io
from django.core.files.uploadedfile import SimpleUploadedFile
import shutil



class ImageTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.user = User.objects.create_user(email='abcdefg@gmail.com', password='pass')
		self.user = User.objects.create_user(email='jfadjfpodfkdkfsdkf@gmail.com', password='pass')
		self.client = Client()

	def test_post_image(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spongebob.png')
		with open(image_path, 'rb') as f:
			image = SimpleUploadedFile('spongebob.png', f.read(), content_type='image/png')
			my_response_post = self.client.post('/api/upload/image', data={'title': 'image_1', 'image': image}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)


		self.assertEqual(True, my_response_content["success"])
		self.assertEqual("image_1", my_response_content["data"]["title"])
		self.assertIsInstance(my_response_content["data"]["url"], str)
		

		

	def test_get_image(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spongebob.png')
		with open(image_path, 'rb') as f:
			image = SimpleUploadedFile('spongebob.png', f.read(), content_type='image/png')
			my_response_post = self.client.post('/api/upload/image', data={'title': 'image_1', 'image': image}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_post_content = json.loads(my_response_post.content)

		my_response_get = self.client.get('/api/upload/image', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		my_response_get_content = json.loads(my_response_get.content)

		self.assertIsInstance(my_response_get_content["data"]["images"], list)
		self.assertEqual(my_response_get_content["data"]["images"][0]["title"], "image_1")
		self.assertIsInstance(my_response_get_content["data"]["images"][0]["url"], str)
		

		

	def test_delete_image_with_existing_id(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spongebob.png')
		with open(image_path, 'rb') as f:
			image = SimpleUploadedFile('spongebob.png', f.read(), content_type='image/png')
			my_response_post = self.client.post('/api/upload/image', data={'title': 'image_1', 'image': image}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		my_response_delete = self.client.delete('/api/upload/image/1', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		my_response_delete_content = json.loads(my_response_delete.content)
		expected_data = {
    					"success": True,
    					"data": {
        					"images": []
    							}
						}

		self.assertEqual(expected_data, my_response_delete_content)
		

		

	def test_delete_image_with_non_existing_id(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spongebob.png')
		with open(image_path, 'rb') as f:
			image = SimpleUploadedFile('spongebob.png', f.read(), content_type='image/png')
			my_response_post = self.client.post('/api/upload/image', data={'title': 'image_1', 'image': image}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		my_response_delete = self.client.delete('/api/upload/image/5', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		my_response_delete_content = json.loads(my_response_delete.content)
		expected_data = {
    					"success": False,
    					"error": "image with that id does not exist"
						}
		self.assertEqual(expected_data, my_response_delete_content)
		

		

	def test_cannot_post_video_for_image(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_vid.mp4')
		with open(video_path, 'rb') as f:
			image = SimpleUploadedFile('sample_vid.mp4', f.read(), content_type='video/mp4')
			my_response_post = self.client.post('/api/upload/image', data={'title': 'image_1', 'image': image}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)


		expected_data = {
    					"success": False,
    					"error": "not a valid image format"
						}
		self.assertEqual(expected_data, my_response_content)
		



	def test_cannot_post_image_with_missing_title_key(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spongebob.png')
		with open(image_path, 'rb') as f:
			image = SimpleUploadedFile('spongebob.png', f.read(), content_type='image/png')
			my_response_post = self.client.post('/api/upload/image', data={'dkdpldkd': 'image_1', 'image': image}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		expected_data = {
    					"success": False,
    					"error": "Title has to be specified in the request as a key"
						}

		self.assertEqual(expected_data, my_response_content)
		

	def test_cannot_post_image_with_missing_image_key(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spongebob.png')
		with open(image_path, 'rb') as f:
			image = SimpleUploadedFile('spongebob.png', f.read(), content_type='image/png')
			my_response_post = self.client.post('/api/upload/image', data={'title': 'image_1', 'scvldsm': image}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		expected_data = {
    					"success": False,
    					"error": "Image has to be specified in the request as a key"
						}

		self.assertEqual(expected_data, my_response_content)
		

	def test_image_value_must_be_in_between_1_and_6(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spongebob.png')
		with open(image_path, 'rb') as f:
			image = SimpleUploadedFile('spongebob.png', f.read(), content_type='image/png')
			my_response_post = self.client.post('/api/upload/image', data={'title': 'image_7', 'image': image}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		expected_data = {
    					"success": False,
    					"error": "not a valid image title"
						}

		self.assertEqual(expected_data, my_response_content)

	def tearDown(self):
		if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../media')):
			shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../media'))
		

class VideoTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='aa@gmail.com', password='pass')
		self.client = Client()

	def test_post_video(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_vid.mp4')
		with open(video_path, 'rb') as f:
			video = SimpleUploadedFile('sample_vid.mp4', f.read(), content_type='video/mp4')
			my_response_post = self.client.post('/api/upload/video', data={'video': video}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)


		self.assertEqual(True, my_response_content["success"])
		self.assertIsInstance(my_response_content["video"]["url"], str)
		

	def test_get_video(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_vid.mp4')
		with open(video_path, 'rb') as f:
			video = SimpleUploadedFile('sample_vid.mp4', f.read(), content_type='video/mp4')
			my_response_post = self.client.post('/api/upload/video', data={'video': video }, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_post_content = json.loads(my_response_post.content)

		my_response_get = self.client.get('/api/upload/video', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		my_response_get_content = json.loads(my_response_get.content)

		self.assertIsInstance(my_response_get_content["videos"], list)
		self.assertIsInstance(my_response_get_content["videos"][0]["video_id"], int)
		self.assertIsInstance(my_response_get_content["videos"][0]["url"], str)
		self.assertEqual(True, my_response_get_content["success"])
		

	def test_delete_video_with_existing_id(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_vid.mp4')
		with open(video_path, 'rb') as f:
			video = SimpleUploadedFile('sample_vid.mp4', f.read(), content_type='video/mp4')
			my_response_post = self.client.post('/api/upload/video', data={'video': video}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		my_response_delete = self.client.delete('/api/upload/video/1', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		my_response_delete_content = json.loads(my_response_delete.content)

		expected_data = {
    					"success": True,
    					"videos": []
						}

		self.assertEqual(expected_data, my_response_delete_content)
		

	def test_delete_video_with_non_existing_id(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_vid.mp4')
		with open(video_path, 'rb') as f:
			video = SimpleUploadedFile('sample_vid.mp4', f.read(), content_type='video/mp4')
			my_response_post = self.client.post('/api/upload/video', data={'video': video}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		my_response_delete = self.client.delete('/api/upload/video/5', HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
		my_response_delete_content = json.loads(my_response_delete.content)
		expected_data = {
    					"success": False,
    					"error": "video with that id does not exist"
						}
		self.assertEqual(expected_data, my_response_delete_content)
		

	def test_cannot_image_for_video(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spongebob.png')
		with open(video_path, 'rb') as f:
			video = SimpleUploadedFile('spongebob.png', f.read(), content_type='image/png')
			my_response_post = self.client.post('/api/upload/video', data={'video': video}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		expected_data = {
    					"success": False,
    					"data": "file is not of type .mp4"
						}
		self.assertEqual(expected_data, my_response_content)
		

	def test_cannot_post_video_with_missing_video_key(self):
		login_response = self.client.post('/api/auth/login', {'email': 'aa@gmail.com', 'password' : 'pass'}, HTTP_ACCEPT='application/json')
		login_response_body = json.loads(login_response.content)
		token = login_response_body['access']  # Gets the token

		video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_vid.mp4')
		print("media: ", os.path.join(os.path.dirname(os.path.abspath(__file__)), '../media') )
		with open(video_path, 'rb') as f:
			video = SimpleUploadedFile('spongebob.png', f.read(), content_type='video/mp4')
			my_response_post = self.client.post('/api/upload/video', data={'amcdklasmd': video}, HTTP_ACCEPT='application/json', **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
			my_response_content = json.loads(my_response_post.content)

		expected_data = {
    					"success": False,
    					"error": "Request must contain video as a key."
						}

		self.assertEqual(expected_data, my_response_content)

	def tearDown(self):
		if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../media')):
			shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../media'))

