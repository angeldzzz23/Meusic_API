from authentication.models import User, Skills, Genres, Genders
from preferences.models import User_Preference_Genders, User_Preference_Skills, User_Preference_Genres, User_Preferences_Globally, User_Preferences_Age, User_Preferences_Distance
from enum import Enum



class List_Fields(Enum):
    SKILLS = 'skills'
    GENRES = 'genres'
    GENDERS = 'genders'

class Dict_Fields(Enum):
    AGES = 'age'
    #DISTANCES = 'distance'

class User_Fields(Enum):
    SKILLS = 'skills'
    GENRES = 'genres'
    GENDERS = 'genders'
    AGES = 'age'
    DISTANCES = 'distances'
    search_globally = 'search_globally'

def get_list_field(user_id, f_name, f_ids): # pass in singular of field_name!!
    field_id = f_name + "_id"       #age_id
    field_name = f_name + "_name"   #age_name
    field_names = []

    if f_name == 'skill':
        field_ids = f_ids if f_ids else User_Preference_Skills.objects.filter(user_id=user_id).values(field_id)
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
        print("gender field_id is", field_ids)
        if field_ids:
            for obj in field_ids:
                the_id = obj if f_ids else obj[field_id]
                x = Genders.objects.filter(gender_id=the_id).values(field_name)
                #field_names.append({'gender_id': the_id, 'gender_name': x[0][field_name]})
                field_names.append(x[0][field_name])
            return field_names

    elif f_name == 'age':
        age_pair_as_list = f_ids if f_ids else User_Preferences_Age.objects.filter(user_id=user_id).values('age_low','age_high')
        print("age get aaaaaaaaaaaaaa", age_pair_as_list)
        #print("age pair as list 1: ", age_pair_as_list)
        #var = User_Preferences_Age.objects.filter(user_id=user_id).values('age_low','age_high')
        #print("This is the current dict", var['age_low'])

        age_low = age_pair_as_list[0]
        print("age_low = age_pair_as_list[0]['age_low']:" , age_low)
        age_high = age_pair_as_list[0]
        print("314343245234wrfrewdf", age_pair_as_list)
        print(age_high)
        print("age_pair_as_list ", age_pair_as_list)
        # if age_low_and_high:
        #     for obj in age_low_and_high:
        #         the_id = obj if f_ids else obj[field_id]
        #         x = User_Preferences_Age.objects.filter(age_id=the_id).values(field_name)
        #         field_names.append({'low': x[0]['age_low'], 'high': x[0]['age_high']})
        #    return field_names
        field_names.append({'age_low': age_low, 'age_high': age_high})
        print("These are the field names: ", field_names)
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
        elif field_name == "genres":
            field_from_db = Genres.objects.filter(genre_id=obj)
        elif field_name == "genders":
            field_from_db = Genders.objects.filter(gender_id=obj)

        if not field_from_db:
            return {'success' : False,
                    'error' : "Could not find one or several " +
                    field_name + " in database."}


