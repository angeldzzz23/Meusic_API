from authentication.models import User, Skills, User_Skills, Genres, User_Genres
from rest_framework import response, status
from enum import Enum


class List_Fields(Enum):
    SKILLS = 'skills'
    GENRES = 'genres'


def get_list_field(email, f_name): # pass in singular of field_name!! 
    user_id = (User.objects.filter(email=email).values('id'))[0]['id']
    field_id = f_name + "_id"
    field_name = f_name + "_name"

    if f_name == 'skill':
        field_ids = User_Skills.objects.filter(user_id=user_id).values(field_id)
        if field_ids:
            field_names = []
            for obj in field_ids:
                the_id = obj[field_id]
                x = Skills.objects.filter(skill_id=the_id).values(field_name)
                field_names.append(x[0][field_name])
            return field_names

    if f_name == 'genre':
        field_ids = User_Genres.objects.filter(user_id=user_id).values(field_id)
        if field_ids:
            field_names = []
            for obj in field_ids:
                the_id = obj[field_id]
                x = Genres.objects.filter(genre_id=the_id).values(field_name)
                field_names.append(x[0][field_name])
            return field_names


def validate_field(field_name, field_list): 
    if not isinstance(field_list, list):
        return {'success' : False, 
                'error' : "Field for " + field_name + " should be in a list."}

    if len(field_list) > 5:
        return {'success' : False, 
                'error' : "Cannot submit more than 5 " + field_name + "."}

    if len(field_list) != len(set(field_list)):
        return {'success' : False, 
                'error' : "Cannot submit duplicate " + field_name + "."}

    for obj in field_list:
        if isinstance(obj, str) and (not obj.isnumeric()):
            return {'success' : False, 
                    'error' : "Please enter numeric " + field_name + "."}

    for obj in field_list:
        if field_name == "skills":
            field_from_db = Skills.objects.filter(skill_id=obj)
        if field_name == "genres":
            field_from_db = Genres.objects.filter(genre_id=obj)

        if not field_from_db:
            return {'success' : False, 
                    'error' : "Could not find one or several " + 
                    field_name + " in database."}
