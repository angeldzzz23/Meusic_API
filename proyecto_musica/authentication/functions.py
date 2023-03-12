from authentication.models import User, Skills, User_Skills, Genres, User_Genres, User_Artists, User_Youtube, User_Vimeo, Nationality, User_Nationality, User_Videos
from rest_framework import response, status
from enum import Enum
import re


class List_Fields(Enum):
    SKILLS = 'skills'
    GENRES = 'genres'
    ARTISTS = 'artists'
    YOUTUBEVIDS = 'youtube_vids'
    VIMEOVIDS = 'vimeo_vids'
    NATIONALITIES = 'nationalities'
    location = "location"
    videos = 'videos'



class User_Fields(Enum):
    USERNAME = 'username'
    EMAIL = 'email'
    FIRSTNAME = 'first_name'
    LASTNAME = 'last_name'
    GENDER = 'gender'
    DOB = 'DOB'
    ABOUTME = 'about_me'
    PASSWORD = 'password'
    SKILLS = 'skills'
    GENRES = 'genres'
    ARTISTS = 'artists'
    YOUTUBEVIDS = 'youtube_vids'
    VIMEOVIDS = 'vimeo_vids'
    NATIONALITIES = 'nationalities'
    location = "location"
    videos = 'videos'


def get_list_field(user_id, f_name, f_ids): # pass in singular of field_name!!
    field_id = f_name + "_id"
    field_name = f_name + "_name"
    field_names = []

    if f_name == 'skill':
        field_ids = f_ids if f_ids else User_Skills.objects.filter(user_id=user_id).values(field_id)
        if field_ids:
            for obj in field_ids:
                the_id = obj if f_ids else obj[field_id]
                x = Skills.objects.filter(skill_id=the_id).values(field_name)
                field_names.append({'skill_id': the_id, 'skill_name': x[0][field_name]})
            return field_names
    elif f_name == 'genre':
        field_ids = f_ids if f_ids else User_Genres.objects.filter(user_id=user_id).values(field_id)
        if field_ids:
            for obj in field_ids:
                the_id = obj if f_ids else obj[field_id]
                x = Genres.objects.filter(genre_id=the_id).values(field_name)
                field_names.append({'genre_id': the_id, 'genre_name': x[0][field_name]})
            return field_names
    elif f_name == 'artist':
            field_ids = User_Artists.objects.filter(user_id=user_id).values(f_name, 'user_artist_id')
            list_field_ids = []
            for obj in field_ids:
                list_field_ids.append({ 'user_artist_id': obj['user_artist_id'],'artist':obj[f_name]})
            return list_field_ids if list_field_ids else None
    elif f_name == 'youtube_vids':
            field_ids = User_Youtube.objects.filter(user_id=user_id).values('youtube_id','video_id')
            list_field_ids = []
            for obj in field_ids:
                list_field_ids.append({"youtube_id":obj['youtube_id'],"video_id": obj['video_id']})
            return list_field_ids if list_field_ids else None
    elif f_name == 'vimeo_vids':
            field_ids = User_Vimeo.objects.filter(user_id=user_id).values('vimeo_id','video_id')
            list_field_ids = []
            for obj in field_ids:
                list_field_ids.append({'vimeo_id':obj['vimeo_id'],"video_id": obj['video_id']})
            return list_field_ids if list_field_ids else None
    elif f_name == 'videos': 
             
            field_ids = User_Videos.objects.filter(user_id=user_id).values('vid_id','video_id')

            list_field_ids = []
            for obj in field_ids:
                list_field_ids.append({'vid_id':obj['vid_id'],"video_id": obj['video_id']})
            return list_field_ids if list_field_ids else None

    elif f_name == 'nationality':
        field_ids = f_ids if f_ids else User_Nationality.objects.filter(user_id=user_id).values(field_id)
        if field_ids:
            for obj in field_ids:
                the_id = obj if f_ids else obj[field_id]
                x = Nationality.objects.filter(nationality_id=the_id).values(field_name)
                field_names.append({'nationality_id': the_id, 'nationality_name': x[0][field_name]})
            return field_names

def validate_field(field_name, field_list):
    if field_name == 'location':
        return None

    if not isinstance(field_list, list):
        return {'success' : False,
                'error' : "Field for " + field_name + " should be in a list."}

    if len(field_list) > 5:
        return {'success' : False,
                'error' : "Cannot submit more than 5 " + field_name + "."}

    if len(field_list) != len(set(field_list)):
        return {'success' : False,
                'error' : "Cannot submit duplicate " + field_name + "."}

    if field_name == "artists":
        return None
    if field_name == 'youtube_vids':
        return None
    if field_name == 'vimeo_vids':
        return None
    if field_name == 'videos':
        return None

    for obj in field_list:
        if isinstance(obj, str) and (not obj.isnumeric()):
            return {'success' : False,
                    'error' : "Please enter numeric " + field_name + "."}


    for obj in field_list:
        if field_name == "skills":
            field_from_db = Skills.objects.filter(skill_id=obj)
        elif field_name == "genres":
            field_from_db = Genres.objects.filter(genre_id=obj)
        elif field_name == "nationalities":
            field_from_db = Nationality.objects.filter(nationality_id=obj)


        if not field_from_db:
            return {'success' : False,
                    'error' : "Could not find one or several " +
                    field_name + " in database."}

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def validate_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
