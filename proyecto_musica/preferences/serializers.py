from preferences.models import User_Preference_Genders, User_Preference_Skills, User_Preference_Genres, User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
from authentication.models import User, Genders, Skills, Genres
from rest_framework import serializers
from preferences.functions import List_Fields, get_list_field
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken


class PreferenceGendersSerializer(serializers.ModelSerializer):
    genders = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('genders',)

    def get_genders(self, obj):
        genders = self.context.get("genders")
        return get_list_field(obj.id, "gender", genders)


class PreferenceSkillsSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields=('skills',)

    def get_skills(self, obj):
        skills = self.context.get("skills")
        return get_list_field(obj.id, "skill", skills)


class PreferenceGenresSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('genres',)

    def get_genres(self, obj):
        genres = self.context.get("genres")
        return get_list_field(obj.id, "genre", genres)


class PreferenceAgeSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        #model = User_Preferences_Age
        model = User
        fields = ('age',)

    def get_age(self, obj):
        age = self.context.get("age")   
        return get_list_field(obj.id, "age", age)

class PreferenceDistanceSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        #model = User_Preferences_Age
        model = User
        fields = ('distance',)

    def get_distance(self, obj):
        distance = self.context.get("distance")   
        return get_list_field(obj.id, "distance", distance)


class PreferenceGloballySerializer(serializers.ModelSerializer):
    search_globally = serializers.SerializerMethodField()

    class Meta:
        #model = User_Preferences_Age
        model = User
        fields = ('search_globally',)

    def get_search_globally(self, obj):
        search_globally = self.context.get("search_globally")   
        return get_list_field(obj.id, "search_globally", search_globally)


class PreferenceEditSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    genders = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    search_globally = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=('skills', 'genres', 'genders', 'age', 'distance', 'search_globally')

    def get_skills(self, obj):
        skills = self.context.get("skills")
        return get_list_field(obj.id, "skill", skills)

    def get_genres(self, obj):
        genres = self.context.get("genres")
        return get_list_field(obj.id, "genre", genres)

    def get_genders(self, obj):
        genders = self.context.get("genders")
        print("Genders: ", genders)   
        return get_list_field(obj.id, "gender", genders)

    def get_age(self, obj):
        age = self.context.get("age")   
        return get_list_field(obj.id, "age", age)

    def get_distance(self, obj):
        distance = self.context.get("distance")   
        return get_list_field(obj.id, "distance", distance)

    def get_search_globally(self, obj):
        search_globally = self.context.get("search_globally")   
        return get_list_field(obj.id, "search_globally", search_globally)
    
    def update(self, instance, validated_data):
        id = instance.id

        for field in List_Fields:
            field_name = field.value
            field_list = self.context.get(field_name)

            if field_list is not None:
                if field_name == 'skills':
                    User_Preference_Skills.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Preference_Skills.objects.create(user_id=id, skill_id=obj)
                elif field_name == 'genres':
                    User_Preference_Genres.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Preference_Genres.objects.create(user_id=id, genre_id=obj)
                elif field_name == 'genders':
                    User_Preference_Genders.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Preference_Genders.objects.create(user_id=id, gender_id=obj)
                elif field_name == 'age':
                    User_Preferences_Age.objects.filter(user_id=id).delete()
                    if len(field_list)!=0:
                        User_Preferences_Age.objects.create(user_id=id, age_low = field_list['low'], age_high = field_list['high'])

                elif field_name == 'distance':
                    User_Preferences_Distance.objects.filter(user_id=id).delete()
                    if len(field_list)!=0:
                        User_Preferences_Distance.objects.create(user_id=id, distance_low = field_list['low'], distance_high = field_list['high'])

                elif field_name == 'search_globally':
                    User_Preferences_Globally.objects.filter(user_id=id).delete()
                    User_Preferences_Globally.objects.create(user_id=id, search_globally = field_list) 
                    
        return instance


