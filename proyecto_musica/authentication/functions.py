from authentication.models import Skills, Genres
from rest_framework import response, status
from enum import Enum


class List_Fields(Enum):
    SKILLS = 'skills'
    GENRES = 'genres'


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
