from authentication.models import User, Skills, Genres, Genders
from preferences.models import User_Preference_Genders, User_Preference_Skills, User_Preference_Genres, User_Preferences_Globally, User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
from enum import Enum



class List_Fields(Enum):
    SKILLS = 'skills'
    GENRES = 'genres'
    GENDERS = 'genders'
    AGES = 'age'
    DISTANCES = 'distance'
    SEARCH_GLOBALLY = 'search_globally'

class User_Fields(Enum):
    SKILLS = 'skills'
    GENRES = 'genres'
    GENDERS = 'genders'
    AGES = 'age'
    DISTANCES = 'distance'
    SEARCH_GLOBALLY = 'search_globally'

def get_list_field(user_id, f_name, f_ids): # f_ids = [1,2,3](value of a field) if field exists in body, 'None' if doesnt exist   f_name = name of a key, i.e. skills, genres...
    field_id = f_name + "_id"       #age_id
    field_name = f_name + "_name"   #age_name
    field_names = []

    if f_name == 'skill':
        field_ids = f_ids if f_ids else User_Preference_Skills.objects.filter(user_id=user_id).values(field_id) # <QuerySet [{'skill_id': 1}, {'skill_id': 2}]>
        if field_ids:
            for obj in field_ids:
                the_id = obj if f_ids else obj[field_id]
                x = Skills.objects.filter(skill_id=the_id).values(field_name)
                field_names.append({'skill_id': the_id, 'skill_name': x[0][field_name]})
            return field_names
    elif f_name == 'genre':
        field_ids = f_ids if f_ids else User_Preference_Genres.objects.filter(user_id=user_id).values(field_id)
        
        if field_ids:
            for obj in field_ids:
                the_id = obj if f_ids else obj[field_id]
                x = Genres.objects.filter(genre_id=the_id).values(field_name)
                field_names.append({'genre_id': the_id, 'genre_name': x[0][field_name]})
            return field_names

    elif f_name == 'gender':
        field_ids = f_ids if f_ids else User_Preference_Genders.objects.filter(user_id=user_id).values(field_id)
        if field_ids:
            for obj in field_ids:
                the_id = obj if f_ids else obj[field_id]
                x = Genders.objects.filter(gender_id=the_id).values(field_name)
                #field_names.append({'gender_id': the_id, 'gender_name': x[0][field_name]})
                field_names.append(x[0][field_name])
            return field_names

    elif f_name == 'age':
        if f_ids:
            field_ids = []
            field_ids.append(f_ids['low'])
            field_ids.append(f_ids['high'])
        else:
            field_ids = list(User_Preferences_Age.objects.filter(user_id=user_id).values_list('age_low','age_high'))
            temp = field_ids.copy()
            field_ids = []
            if len(temp) == 0:
                return 
            for element in temp[0]:
                field_ids.append(element)

        if field_ids:
            field_names.append({'low': field_ids[0], 'high': field_ids[1]})
            return field_names[0]

    elif f_name == 'distance':
        if f_ids:
            field_ids = []
            field_ids.append(f_ids['low'])
            field_ids.append(f_ids['high'])
        else:
            field_ids = list(User_Preferences_Distance.objects.filter(user_id=user_id).values_list('distance_low','distance_high'))
            temp = field_ids.copy()
            field_ids = []
            if len(temp) == 0:
                return 
            for element in temp[0]:
                field_ids.append(element)

        if field_ids:
            field_names.append({'low': field_ids[0], 'high': field_ids[1]})
            return field_names[0]

    elif f_name == 'search_globally':
        if f_ids:
            field_ids = []
            field_ids.append(f_ids) 
        else:
            field_ids = list(User_Preferences_Globally.objects.filter(user_id=user_id).values_list('search_globally'))
            temp = field_ids.copy()
            field_ids = []
            if len(temp) == 0:
                return 
            for element in temp[0]:
                field_ids.append(element)

        if field_ids:
            field_names.append(field_ids[0])
            return field_names[0]

   

def validate_field(field_name, field_list):
    if (field_name == 'genres' or field_name == 'genders' or field_name == 'skills'):
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
            if not isinstance(obj, int):
                return {'success' : False,
                    'error' : "Each value must be an integer in " + field_name + "."}
                    
            if isinstance(obj, str) and (not obj.isnumeric()):
                return {'success' : False,
                        'error' : "Please enter numeric " + field_name + "."}

        for obj in field_list:
            if field_name == "skills":
                field_from_db = Skills.objects.filter(skill_id=obj)
            elif field_name == "genres":
                field_from_db = Genres.objects.filter(genre_id=obj)
            elif field_name == "genders":
                field_from_db = Genders.objects.filter(gender_id=obj)

            if not field_from_db:
                return {'success' : False,
                        'error' : "Could not find one or several " +
                        field_name + " in database."}

    if (field_name == 'search_globally'):
        if not isinstance(field_list, bool):
            return {'success' : False,
                    'error' : "Field for " + field_name + " should be a boolean."}



    if (field_name == 'age' or field_name == 'distance'):
        if not isinstance(field_list, dict):
            return {'success' : False,
                    'error' : field_name + " must be a dictionary."}
        if len(field_list) != 2:
            return {'success' : False,
                    'error' : "incorrect amount of keys in " + field_name + "."}
        for obj in field_list:
            if (obj != "low") and (obj != "high"):
                return {'success' : False,
                    'error' : "low and high are the only allowed keys for " + field_name + "."}

        for obj in field_list:
            if not isinstance(field_list[obj], int):
                return {'success' : False,
                    'error' : "Each value must be an integer in " + field_name + "."}

        if  field_list["low"] > field_list["high"]:
            return {'success' : False,
                    'error' : "low must be <= high in " + field_name + "."}


