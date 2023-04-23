from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import response
from rest_framework import response, status, permissions
from michaelscarn.functions import deleteUser
from django.core.files import File
from newsfeed.models import User_Matches,User_Likes
from preferences.models import User_Preference_Genders, User_Preference_Skills, User_Preference_Genres
from preferences.models import User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
from authentication.serializers import RegisterSerializer

from authentication.models import User, User_Skills, Skills, Genres, User_Genres, User_Artists, Genders, Verification, Nationality, User_Nationality

from api.serializers import PictureSerialiser, PicturesSerializer,Videoerialiser, VideosSerializer

from api.models import Images, Videos
from rest_framework.response import Response
import os
from pathlib import Path
import json
import shutil
from proyecto_musica.settings import BASE_DIR


# Create your views here.
# this is the app to test user info 


# Create your views here.


# the michael scarn app is in charge of 
#all the testing endpoints 

import random
from random import randrange

class FakeUser:
    def __init__(self, skills=None, genres=None, nationalities=None, genders=None):
        self.skills = skills
        self.genres = genres
        self.nationalities = nationalities
        self.genders = genders
        self.context = {}
        self.fullUser = {}

    def initializeUser(self, fname, lname, email, username, dateOfBirth, bio):
        self.fullUser = {"email":email, 'username': username, "password":"123456","first_name": fname, "last_name":lname, "DOB": dateOfBirth, "gender": None, "about_me": bio
                }


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
        self.fullUser['gender'] = userGender

        self.fullUser['context'] = {
            "skills": userSkills,
            "genres": userGenres,
            "nationalities":userNationalities, 
            "artists": ["kakakmakakkaka", "akkakakkaka", "jnnbn23j32ajaj"],
            "videos": ["wAjHQXrIj9o", "WuVJMfhpdUk", "297519326"]
        }






class CreatingFakeData(GenericAPIView):

    def delete(self, request): 
        # getting all of the users 
         # delete the user likes 
         # User_Genres.objects.all().delete()
        User_Likes.objects.all().delete()


        # delete the user matches
        User_Matches.objects.all().delete() 

        # delete the preferences 
        # prefrences 
        User_Preference_Genders.objects.all().delete() 
        User_Preference_Skills.objects.all().delete() 
        User_Preference_Genres.objects.all().delete() 
        User_Preferences_Age.objects.all().delete() 
        User_Preferences_Distance.objects.all().delete() 
        User_Preferences_Globally.objects.all().delete() 

        user = User.objects.all()

        for aUser in user:
             deleteUser(str(aUser.id))

        datos = {'success':True}

        return response.Response(datos, status=status.HTTP_201_CREATED)

    def post(self, request,id):
    	# datos = {'success':True}
       # return response.Response(datos, status=status.HTTP_201_CREATED)
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

        elif id == "users": 


            skills = list(Skills.objects.all())
            genres = list(Genres.objects.all())
            nat = list(Nationality.objects.all())
            genders = list(Genders.objects.all())
            userFactory = FakeUser(skills, genres, nat, genders)


            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            file = open(os.path.join(__location__, 'fakeuserlist.txt'))
            count = 0
            for line in file:
                userInfo = line.replace('\n','').split(' ')
                # print('line ',userInfo)
                fname = userInfo[0]
                lname = userInfo[1]
                email = userInfo[2]
                username = userInfo[3]
                dateOfBirth = userInfo[4]
                bio = userInfo[5]


                userFactory.initializeUser(fname, lname, email, username, dateOfBirth, bio)
                userFactory.createUserFieldLists()
                
                serializer = RegisterSerializer(data=userFactory.fullUser,context=userFactory.fullUser['context'])
                if serializer.is_valid():
                    serializer.save()

                try:
                    user_obj = User.objects.get(username=username)
                except User.DoesNotExist:
                    res = {'success' : False, 'error' : "user with that username does not exist."}
                    return response.Response(res, status=status.HTTP_400_BAD_REQUEST)

                img = request.FILES["image"]

                jd = request.data

                imageNames = ["image_1","image_2","image_3","image_4","image_5","image_6"]

                for imageName in imageNames:
                    jd['title'] = imageName
                    picture_serializer = PictureSerialiser(data=jd, context={'user': user_obj, 'img' : img, 'request': request})
                    if picture_serializer.is_valid():
                        picture_serializer.save()
                        datos = {'success':True,'data':picture_serializer.data}

                video = request.FILES["video"]

                # checking if video is 
                if video:
                    filename = video.name

                    if  (filename.endswith('.MP4') or filename.endswith('.mp4')) == False :
                        datos = {'success':False,'data':"file is not of type .mp4"}
                        return response.Response(datos, status=status.HTTP_400_BAD_REQUEST)


                video_serializer = Videoerialiser(data=jd, context={'user': user_obj, 'vid' : video, 'request': request, 'caption': 'This is a fake caption'})

                if video_serializer.is_valid():
                    video_serializer.save()

            # generating preferences for each user 
        elif id == 'preferences': 
            print('preferences')

        datos = {'success':True}
        return response.Response(datos, status=status.HTTP_201_CREATED)



class GenerateFakeDataPart2(GenericAPIView):
    def post(self, request):
        datos = {'success':True}
        return response.Response(datos, status=status.HTTP_201_CREATED)




