from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentication.serializers import RegisterSerializer
from authentication.serializers import EditSerializer
from authentication.serializers import LoginSerializer, CookieTokenRefreshSerializer, WithNoCookieTokenRefreshSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from authentication.models import User, User_Skills, Skills, Genres, User_Genres, User_Artists, Genders, Verification, Nationality, User_Nationality
from authentication.functions import validate_field, List_Fields, User_Fields, deleteUser
from authentication.Util import Util
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers  import TokenObtainSerializer
from rest_framework_simplejwt.serializers  import TokenRefreshSerializer


from api.models import Images
from api.models import Videos
from rest_framework.response import Response
import os
from pathlib import Path

import json
import shutil
import os
from proyecto_musica.settings import BASE_DIR

from django.utils.timezone import utc
import datetime

from django.contrib.auth import login

from rest_framework_simplejwt.serializers import TokenObtainSerializer

from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from authentication.functions import validate_email
from preferences.serializers import PreferenceEditSerializer

# this uses a cookie
# this is in charge of refreshing the user's token
class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            response.set_cookie('access', response.data['access'], max_age=cookie_max_age, httponly=True )

        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


# documentation
#https://github.com/jazzband/djangorestframework-simplejwt/issues/71  -  LoranKloeze comment
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/rest_framework_simplejwt.html
class CookieTokenRefreshView2(TokenRefreshView):
    serializer_class = WithNoCookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):

        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            response.set_cookie('access', response.data['access'], max_age=cookie_max_age, httponly=True )


        return super().finalize_response(request, response, *args, **kwargs)


class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EditSerializer

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        serialized_data = (serializer.data).copy()
        if 'gender' in serializer.data:
            serialized_data.pop('gender')

        res = {'success' : True, 'user': serialized_data}
        return response.Response(res)

    def patch(self, request):
        jd = request.data
        id = request.user.id
        context = {}

        try:
            user_obj = User.objects.get(id=id)
        except User.DoesNotExist:
            res = {'success' : False, 'error' : "User id does not exist."}
            return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

        # check body fields
        request_keys = list(jd.keys())
        allowed_keys = [e.value for e in User_Fields]
        for key in request_keys:
            if key not in allowed_keys:
                res = {'success' : False,
                        'error' : "Wrong parameter(s) passed in request."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

        for field in List_Fields:
            field_name = field.value

            if field_name in jd:
                field_list = jd[field_name]
                res = validate_field(field_name, field_list)
                if res:
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)
                context[field_name] = field_list

        serializer = EditSerializer(user_obj, data=jd,
                                           context=context, partial=True)

        if serializer.is_valid():
            serializer.save()
            # only return fields that were modified
            serialized_data = (serializer.data).copy()

            for field in serializer.data:
                if field not in jd and field != 'gender_name':
                    serialized_data.pop(field)

            # implementing the is set up
            if user_obj.DOB and user_obj.username:
                if not user_obj.is_setup:
                    user_obj.is_setup = True
                    user_obj.save()
            else:
                if  user_obj.is_setup:
                    user_obj.is_setup = True
                    user_obj.save()

            if 'gender' in jd:
                serialized_data.pop('gender')

            if 'gender' not in jd:
                serialized_data.pop('gender_name')

            res = {'success' : True, 'user': serialized_data}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : False, 'user': serializer.errors}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)


    # deleting the use
    def delete(self, request):

        id = request.user.id
        User_Genres.objects.filter(user_id=id).delete()
        User_Skills.objects.filter(user_id=id).delete()
        User_Artists.objects.filter(user_id=id).delete()
        User_Nationality.objects.filter(user_id=id).delete()

        # deleting the pics
        pics = Images.objects.filter(user_id=id)


        for pic in pics:
            pic.image.delete()
            pic.delete()

        # deleting the videos
        vids = Videos.objects.filter(user_id=id)

        for video in vids:
            video.video.delete()
            video.delete()


        # TODO: delete its media folder
        file_location = os.path.join(BASE_DIR, 'media/videos/' + str(id))
        p = Path(file_location)
        if p.is_dir():
            shutil.rmtree(file_location, ignore_errors = False)



        # deletes image folder
        # delete its images folder
        file_location = os.path.join(BASE_DIR, 'media/photos/' + str(id))
        p = Path(file_location)

        if p.is_dir():
            shutil.rmtree(file_location, ignore_errors = False)

        #delete user
        usr = User.objects.get(id = id)
        usr.delete()






        res = {'success' : True, 'message': 'user has been deleted'}
        return response.Response(res, status=status.HTTP_201_CREATED)



class RegisterAPIView(GenericAPIView):

    serializer_class= RegisterSerializer

    def post(self, request):
        jd = request.data
        context = {}

        # check body fields
        request_keys = list(jd.keys())
        allowed_keys = [e.value for e in User_Fields]
        for key in request_keys:
            if key not in allowed_keys:
                res = {'success' : False,
                        'error' : "Wrong parameter(s) passed in request."}
                return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)

        for field in List_Fields:
            field_name = field.value

            if field_name in jd:
                field_list = jd[field_name]
                res = validate_field(field_name, field_list)
                if res:
                    return response.Response(res, status=status.HTTP_401_UNAUTHORIZED)
                context[field_name] = field_list

        serializer = self.serializer_class(data=jd,
                                           context=context)

        if serializer.is_valid():
            serializer.save()

            serialized_data = (serializer.data).copy()
            serialized_data.pop('gender')

            email = serialized_data['email']

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                print('user does not exist')

            if serialized_data['username'] and serialized_data['DOB']:
                user.is_setup = True
                user.save()

            else:
                print('we do not have a username and we do not have a DOB')



            res = {'success' : True, 'user': serialized_data}
            return response.Response(res, status=status.HTTP_201_CREATED)

        res = {'success' : False, 'user': serializer.errors}
        return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

# this used to log in the user
# response gives us the token if it is a valid login
import jwt
from django.conf import settings

class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class= LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user=authenticate(username=email, password=password)

        if user:
            serializer=self.serializer_class(user)

            refresh = RefreshToken.for_user(user)

            newdict =  {}
            newdict['success'] = True
            newdict['access'] = serializer.data['token']

            newdict.update({'refresh': str(refresh)})

            # creating the type of response
            response = Response(newdict, status.HTTP_200_OK)
            # setting the cookies here
            response.set_cookie(key='access', value=user.token, httponly=True)
            response.set_cookie(key='refresh_token', value=refresh, httponly=True)

            return response


        datos = {'success': False,'message': "invalid credentials, try again"}
            # return response.Response(serializer.data, status.HTTP_200_OK)
        response = Response(datos, status.HTTP_401_UNAUTHORIZED)
        return response


# verifying email when creating an account
class VerifyEmail(GenericAPIView):
    def get(self, request):
        datos = {'codigo':"400",'message': "a message"}
        return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

    # this post is in charge of sending an email
    def post(self, request):
        jd = request.data

        if 'email' not in jd:
            datos = {
                        "Success": False,
                        "Message": "Please include a verification email"
                    }
            return response.Response(datos, status.HTTP_400_BAD_REQUEST)

        elif 'email' in jd and 'code' not in jd:
            email = jd['email']

            if (validate_email(email) == False):
                return response.Response({"Success": False, "Message": "Please enter a valid email address."}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).count() > 0:
                datos = {'success':False,'message': "an account with that email already exists"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            # check if email exists in database
            verCodeObj = Verification.objects.filter(email=email)
            if verCodeObj.count() > 0:
                Verification.objects.filter(email=email).delete()

            code = Util.random_with_N_digits(6) # generate code
            email_body = 'Hi, this is your confirmation code. It expires in 5 minutes.\n' + str(code)
            dat = {'email_body':email_body, 'to_email':email, 'email_subject':'Verify your email'}
            Verification.objects.create(code=code, email=email)
            Util.send_email(dat)
            datos = {'success':True,'message': "confirmation code was sent"}
            return response.Response(datos, status=status.HTTP_201_CREATED)

        elif 'code' in jd and 'email' in jd:
            email = jd['email']
            code = jd['code']

            if (validate_email(email) == False):
                return response.Response({"Success": False, "Message": "Please enter a valid email address."}, status=status.HTTP_400_BAD_REQUEST)

            # just in case that email is already verified
            if User.objects.filter(email=email).count() > 0:
                datos = {'success':False,'message': "an account with that email is already verified"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            verificationObj = Verification.objects.get(email=email)


            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = (now - verificationObj.created_at) # converted to
            if timediff <= datetime.timedelta(minutes=5):
                if verificationObj.code == int(code):
                    datos = {'success':True,'message': "email was confirmed"}
                    return response.Response(datos, status=status.HTTP_201_CREATED)
                else:
                    datos = {'success':False,'message': "invalid code"}
                    return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)
            else:
                # this meaans time has expired
                Verification.objects.filter(email=email).delete()
                datos = {'success':False,'message': "Time has expired. Please get a new token"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

        # send code to email

# this view is used to reset the password of the user
class ForgotPassword(GenericAPIView):
    def post(self, request):
        # if code equals to code that we have saved
        # check if there is an email
        jd = request.data

        # verify that that we have enail
        if 'email' not in jd:
            # TODO add serializer
            datos = {'success':False,'error': "no email"}
            return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

        # check if the email exists in out database
        tot_users = User.objects.filter(email=jd['email']).count()

        if tot_users != 1:
            datos = {'success':False,'error': "not a valid user"}
            return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

        email = jd['email']

        verCodeObj = Verification.objects.filter(email=email)
        if verCodeObj.count() > 0:
            Verification.objects.filter(email=email).delete()


        code = Util.random_with_N_digits(6) # generate code
        email_body = 'Hi, this is your confirmation code. It expires in 5 minutes.\n' + str(code)
        dat = {'email_body':email_body, 'to_email':email, 'email_subject':'Verify your email'}
        Verification.objects.create(code=code, email=email)
        Util.send_email(dat)
        # now here we send the code to their email

        '''
        user = User.objects.get(email=jd['email'])

        # this code right here to reset the password
        token=RefreshToken.for_user(user).access_token
        '''

        datos = {'success':True,'message': 'code has been sent'}
        return response.Response(datos, status=status.HTTP_201_CREATED)

class VerifyForgotPassword(GenericAPIView):
    # this will return code that can be used to edit the password
    def get(self, request):
        datos = {'success':True,'message': "wowowowowowoowowowowow"}
        return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        jd = request.data

        if ('code' not in jd) or ('email' not in jd):
            return response.Response({"Success": False, "Message": "Please verify presence of email and code"}, status=status.HTTP_400_BAD_REQUEST)

        if 'code' in jd and 'email' in jd:
            email = jd['email']
            code = jd['code']
            # check if a verification code has been sent
            if Verification.objects.filter(email=email).count() == 0:
                datos = {'success':False,'message': "no code has been sent"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            verificationObj = Verification.objects.get(email=email)

            if verificationObj.code != int(code):
                datos = {'success':False,'message': "invalid token"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = (now - verificationObj.created_at) # converted to
            if timediff <= datetime.timedelta(minutes=5):
                if verificationObj.code == int(code):
                    user = User.objects.get(email=jd['email'])
                    # this code right here to reset the password
                    token=RefreshToken.for_user(user).access_token

                    datos = {'success':True,'message': str(token)}
                    return response.Response(datos, status=status.HTTP_201_CREATED)
                else:
                    datos = {'success':False,'message': "invalid code"}
                    return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)
            else:
                # this meaans time has expired
                Verification.objects.filter(email=email).delete()
                datos = {'success':False,'message': "Time has expired. Please get a new token"}
                return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(email=jd['email'])
        # this code right here to reset the password
        token=RefreshToken.for_user(user).access_token

        datos = {'success':False,'token': str(token)}

        return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)


class verifyIsSetUp(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        user = request.user

        json = {}

        if user.is_setup:
            json['is_setup'] = True
        else:
            json['is_setup'] = False

        datos = {'success':True,'user': json}
        return response.Response(datos, status=status.HTTP_201_CREATED)


# class CreatingFakeData2(GenericAPIView):
    # creating a
    # def post(self, request): 




import random
from random import randrange


class FakeUser:
    def __init__(self, skills=None, genres=None, nationalities=None, genders=None):
        self.skills = skills
        self.genres = genres
        self.nationalities = nationalities
        self.genders = genders
        self.context = {}


    def createMisc(self,objectsToChooseFrom, type):
        size = randrange(6)
        userSize = 0 
        skills = []
        if type == 'skills':
            while userSize < size:
                randomSkill = random.choice(objectsToChooseFrom)
                objectsToChooseFrom.remove(randomSkill)
                skills.append(randomSkill.skill_id)
                userSize = userSize + 1
            return skills
        elif type == 'genres':
            while userSize < size:
                randomSkill = random.choice(objectsToChooseFrom)
                objectsToChooseFrom.remove(randomSkill)
                skills.append(randomSkill.genre_id)
                userSize = userSize + 1
            return skills
        elif type == 'nationality':
            while userSize < size:
                randomSkill = random.choice(objectsToChooseFrom)
                objectsToChooseFrom.remove(randomSkill)
                skills.append(randomSkill.nationality_id)
                userSize = userSize + 1
            return skills
        elif type == 'gender':
            chosenGender = random.choice(objectsToChooseFrom)
            return chosenGender.gender_id

    def createUserFieldLists(self):
        # skills 
        userSkills = self.createMisc(self.skills.copy(),'skills')
        # genres 
        userGenres = self.createMisc(self.genres.copy(), 'genres')

        # nationalities
        userNationalities = self.createMisc(self.nationalities.copy(), 'nationality')

        # gender 
        userGender = self.createMisc(self.genders.copy(), 'gender')
        # setting the context 

        mark = { "email":"marklovestheworld@gmail.com", 'username': 'heyitsmark', "password":"123456","first_name": "1234 ", "last_name":"fffan", "DOB": "1999-06-22", "gender": userGender, "about_me": "I created myspace!!!",
            "context" : {
            "skills": userSkills,
            "genres": userGenres,
            "nationalities":userNationalities, 
            "artists": ["kakakmakakkaka", "akkakakkaka", "jnnbn23j32ajaj"],
            "videos": ["aaaa", "aaaa", "dddwd"]
            },
            }
         

        return mark



class CreatingFakeData(GenericAPIView):

    def delete(self, request): 
        # getting all of the users 
        user = User.objects.all()

        for aUser in user:
             deleteUser(str(aUser.id))

        datos = {'success':True}

        return response.Response(datos, status=status.HTTP_201_CREATED)

    def post(self, request,id):
        # point = Locations.objects.all()[0]
        #
        # print(point.point.x)
        # print(point.point.y)
        #
        #
        # user = User.objects.all()[2]
        # point = Point(float(30.5), float(32.5), srid=4326)
        # p = Locations(point=point, user=user)
        # p.save()

        # # create admin user
        # User.objects.create_user(email="admin@gmail.com", password="sheep787", is_staff=True)

        # create skills, genres, nationalities, gen
        if id == 'misc':
            Skills.objects.all().delete()
            Genres.objects.all().delete()
            Nationality.objects.all().delete()
            Genders.objects.all().delete()
            nationalities = ["Mexico", "Argentina", "Colombia","Peru","Venezuela","Chile","Ecuador","Bolivia","Paraguay","Uruguay","Guyana","Suriname","French Guiana","Falkland Islands"]
            skills = ["Singer", "Song Writer", "Music Producer", "Recording Engineer", "Session Musician", "Artist Manager", "Tour Manager", "Music Teacher", "Graphic Desinger", "Baterista", "Booking Agent", "Composer",
                    "Public Relations", "Social Media", "Film Composer", "Music Director"]
            genres = ["Regional", "R&B", "Latin", "Rock", "Pop", "Hip hop music", "Rock music", "Rhythm and blues", "Soul music", "Reggae", "Country", "Funk", "Folk music", "Jazz", "Disco", "Electronic music", "Blues", "Bachata"]
            genders = ["Male", "Female", "Agender", "Bigender", "Cisgender", "Gender Expression", "Gender Fluid", "Genderqueer", "Gender Variant", "Mx.", "Non-Binary", "Passing", "Third Gender", "Transgender", "Transgender woman", "Two-Spirit"]

                  #  creating the Skills
            for skill in skills:
                p = Skills(skill_name=skill)
                p.save()

        # creating the Genres
            for genre in genres:
                p = Genres(genre_name=genre)
                p.save()

        # creating nationalities
            for nationality in  nationalities:
                p = Nationality(nationality_name=nationality)
                p.save()

        # creating Genders
            for gender in genders:
                p = Genders(gender_name=gender)
                p.save()


        def createMisc(objectsToChooseFrom, type):
            
            if type == 'skills':
                size = randrange(6)
                userSize = 0 
                skills = []
                while userSize < size:
                    randomSkill = random.choice(objectsToChooseFrom)
                    objectsToChooseFrom.remove(randomSkill)
                    skills.append(randomSkill.skill_id)
                    userSize = userSize + 1
                return skills

# 
        # list(Skills.objects.all()
        # createMisc(), 'skills')

        # print()





        if id == "users": 

            skills = list(Skills.objects.all())
            genres = list(Genres.objects.all())
            nat = list(Nationality.objects.all())
            genders = list(Genders.objects.all())


            userFactory = FakeUser(skills, genres, nat, genders)
            print(userFactory.createUserFieldLists())


            # (self, skills=None, genres=None, nationalities=None, genders=None):


            user = userFactory.createUserFieldLists()
            context = user['context']

#
            serializer = RegisterSerializer(data=user,context=context)

            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)


        # # everything but the videos get added
            # generate fake skills 

            # size = randrange(6)
            # userSize = 0 
            # skills = []
            # skillsObjects = list(Skills.objects.all())
            # while userSize < size:
            #     randomSkill = random.choice(skillsObjects)
            #     skillsObjects.remove(randomSkill)
            #     skills.append(randomSkill.skill_id)
            #     userSize = userSize + 1

            # print(skills)





            


            # print("hello")
            # skills = Skills.objects.values('skill_id').distinct()[:5]
            # print(skills)

            # print('hahah')
            # skills = Skills.objects.values('skill_id').distinct()
            # print(skills)

            # while userSize < size: 
            #     randomSkill = random.choice(skillsObjects).skill_id
            #     if randomSkill not in skills: 
            #         skills.append(randomSkill)
            #         userSize += 1

            # print(skills)

            # selectedSkills = random.sample(skillsObjects, 5)


            # for sk in selectedSkills: 
            #     print(sk.skill_id)


            # print(typeselectedSkills)

            # for skillss in skillsObjects:
                # print(skillss.skill_id)
            # print(type(skillsObjects))
            # print(str(skillsObjects))


        

            # random_items = random.sample(items, 3)
            


            # if you want only a single random item
            # random_item = random.choice(skillsObjects)

            # print(random_item.skill_id)




            # skills = []

            # generate fake nationalities 

            # generate fake genres



            # mark = { "email":"marklovestheworld@gmail.com", 'username': 'heyitsmark', "password":"123456","first_name": "1234 ", "last_name":"fffan", "DOB": "1999-06-22", "gender": 1, "about_me": "I created myspace!!!",
            # "context" : {
            # "skills": [1,2,3],
            # "genres": [1,2],
            # "nationalities":[1,2], 
            # "artists": ["kakakmakakkaka", "akkakakkaka", "jnnbn23j32ajaj"],
            # "videos": ["aaaa", "aaaa", "dddwd"]
            # },
            # }

            # context = mark['context']

            # serializer = RegisterSerializer(data=mark,context=context)

            # if serializer.is_valid():
            #     serializer.save()






            # mark_preferences = {
            #     "skills": [1,2,3],
            #     "genres": [1,2,3],
            #     "genders": [1],
            #     "age": {
            #         "low": 14,
            #         "high": 22
            #     },
            #     "distance": {
            #         "low": 22,
            #         "high": 50
            #     }
            # }









            # steve = {"email": "stevehatestheworld@gmail.com", "password" : "123456", "username": "stevejobs", "first_name": "Steve", "last_name":"Jobs", "DOB": "1999-06-22", "gender": 1, "artists": ["kakakmakakkaka", "akkakakkaka", "jnnbn23j32ajaj"], "about_me": "I created apple!!!", "youtube_vids": ["abc", "ajkajkajajjaja"], "vimeo_vids": ["1234355", "3456"],  "context":  {
            # "genres": [3,4],
            # "skills": [4,5],
            # "nationalities":[1]
            # }
            # }


            # steve_preferences = {
            #     "skills": [1,2,3],
            #     "genres": [1,2,3],
            #     "genders": [1],
            #     "age": {
            #         "low": 14,
            #         "high": 22
            #     },
            #     "distance": {
            #         "low": 22,
            #         "high": 50
            #     }
            # }


            # bill = {
            # "email": "billgates@gmail.com", "password" : "123456", "username": "billgates", "first_name": "Steve", "last_name":"Jobs", "DOB": "1999-06-22", "gender": 1, "artists": ["kakakmakakkaka", "akkakakkaka", "jnnbn23j32ajaj"], "about_me": "I created apple!!!", "youtube_vids": ["abc", "ajkajkajajjaja"], "vimeo_vids": ["1234355", "3456"],
            # "context": {
            #     "skills": [1,2],
            #     "nationalities":[1],
            #     "genres": [1,2,4]
            #     }
            # }

            # bill_preferences = {
            #     "skills": [1,2,3],
            #     "genres": [1,2,3],
            #     "genders": [1],
            #     "age": {
            #         "low": 14,
            #         "high": 22
            #     },
            #     "distance": {
            #         "low": 22,
            #         "high": 50
            #     }
            # }


            # sam = {
            # "email": "samaltman@gmail.com", "password" : "123456", "username": "samaltman", "first_name": "Sam", "last_name":"Altman", "DOB": "1999-06-22", "gender": 1, "artists": ["kakakmakakkaka", "akkakakkaka", "jnnbn23j32ajaj"], "about_me": "I created apple!!!", "youtube_vids": ["abc", "ajkajkajajjaja"], "vimeo_vids": ["1234355", "3456"],
            # "context": {
            #     "skills": [3,4],
            #     "genres": [1,2],
            #     "nationalities":[1]
            # }
            # }

            # sam_preferences = {
            #     "skills": [1,2,3],
            #     "genres": [1,2,3],
            #     "genders": [1],
            #     "age": {
            #         "low": 14,
            #         "high": 22
            #     },
            #     "distance": {
            #         "low": 22,
            #         "high": 50
            #     }
            # }

            # david = {"email": "davidzambrano@gmail.com", "password" : "123456", "username": "davidzzz23", "first_name": "David", "last_name":"Zambrano", "DOB": "1999-06-22", "gender": 1, "artists": ["kakakmakakkaka", "akkakakkaka", "jnnbn23j32ajaj"], "about_me": "I created apple!!!", "youtube_vids": ["abc", "ajkajkajajjaja"], "vimeo_vids": ["1234355", "3456"], "context": {
            # "skills": [3,6,7],
            # "genres": [4],
            # "nationalities":[1]
            # }
            #     }

            # david_preferences = {
            #     "skills": [1,2,3],
            #     "genres": [1,2,3],
            #     "genders": [1],
            #     "age": {
            #         "low": 14,
            #         "high": 22
            #     },
            #     "distance": {
            #         "low": 22,
            #         "high": 50
            #     }
            # }

            # total_users = [mark, steve, bill, sam, david]
            # jd = {
            #     "skills": [1,2,3],
            #     "genres": [1,2,3],
            #     "genders": [1],
            #     "age": {
            #         "low": 14,
            #         "high": 22
            #     },
            #     "distance": {
            #         "low": 22,
            #         "high": 50
            #     }
            # }

            #  # loop through all of the users and create them
            # for user in total_users:
            #     context = {}

            #     serializer = RegisterSerializer(data=user,context=context)

            #     if serializer.is_valid():
            #         serializer.save()
            #         print("success",user['username'] )

            #     else:
            #         datos = {'success':False}
            #         return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)

            # # initialize the preferences of the user
            # # Refactor this later on
            # for user in total_users:

            #     if user['email'] == "marklovestheworld@gmail.com":
            #         user_obj = User.objects.get(email="marklovestheworld@gmail.com")
            #         serializer = PreferenceEditSerializer(user_obj, data=jd,
            #                                            context=jd, partial=True)
            #         if serializer.is_valid():
            #             serializer.save()

            #         else:
            #             print("there is an error with the serializer for", user_obj)


            #     elif user['email'] == "stevehatestheworld@gmail.com":
            #         user_obj = User.objects.get(email="stevehatestheworld@gmail.com")
            #         serializer = PreferenceEditSerializer(user_obj, data=jd,
            #                                            context=jd, partial=True)
            #         if serializer.is_valid():
            #             serializer.save()

            #         else:
            #             print("there is an error with the serializer for", user_obj)

            #     elif user['email'] == "billgates@gmail.com":
            #         user_obj = User.objects.get(email="billgates@gmail.com")
            #         serializer = PreferenceEditSerializer(user_obj, data=jd,context=jd, partial=True)

            #         if serializer.is_valid():
            #             serializer.save()

            #         else:
            #             print("there is an error with the serializer for", user_obj)

            #     elif user['email'] == "samaltman@gmail.com":
            #         user_obj = User.objects.get(email="samaltman@gmail.com")
            #         serializer = PreferenceEditSerializer(user_obj, data=jd,
            #                                            context=jd, partial=True)
            #         if serializer.is_valid():
            #             serializer.save()

            #         else:
            #             print("there is an error with the serializer for", user_obj)


            #     elif user['email'] == "davidzambrano@gmail.com":
            #         user_obj = User.objects.get(email="davidzambrano@gmail.com")
            #         serializer = PreferenceEditSerializer(user_obj, data=jd,
            #                                            context=jd, partial=True)
            #         if serializer.is_valid():
            #             serializer.save()
            #         else:
            #             print("there is an error with the serializer for", user_obj)




        datos = {'success':True}
        return response.Response(datos, status=status.HTTP_201_CREATED)
