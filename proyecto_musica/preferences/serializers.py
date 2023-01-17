from preferences.models import User_Preference_Genders, User_Preference_Skills, User_Preference_Genres, User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
from authentication.models import User, Genders, Skills, Genres, Genders
from rest_framework import serializers
from preferences.functions import List_Fields, get_list_field, Dict_Fields
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken


class PreferenceGendersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genders
        fields = ('gender_id','gender_name',)
    def get_genders(self, obj):
        return Genders.objects.all().order_by('gender_name').values('gender_id','gender_name')
    def create(self, validated_data):
        gender =  Genders.objects.create(**validated_data)
        return gender

class AllPreferenceGendersSerializer(serializers.ModelSerializer):
    genders = serializers.SerializerMethodField()
    class Meta:
        model = Genders
        fields = ('genders',)
    def get_genders(self, obj):
        nums = Genders.objects.all().order_by('gender_name').values('gender_id','gender_name')
        return  nums

class PreferenceSkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skills
        fields = ('skill_id','skill_name',)
    def get_skills(self, obj):
        return Skills.objects.all().order_by('skill_name').values('skill_id','skill_name')
    def create(self, validated_data):
        skill =  Skills.objects.create(**validated_data)
        return skill
    def destroy(self,request):
        print("here")
        return {}


class AllPreferenceSkillsSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    class Meta:
        model = Skills
        fields = ('skills',)
    def get_skills(self, obj):
        nums = Skills.objects.all().order_by('skill_name').values('skill_id','skill_name')
        return  nums


class PreferenceGenresSerializer(serializers.ModelSerializer):
    # skills = serializers.SerializerMethodField()

    class Meta:
        model = Genres
        fields = ('genre_id','genre_name',)

    def create(self, validated_data):
        genres =  Genres.objects.create(**validated_data)
        return genres


class AllPreferenceGenresSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Genres
        fields = ('genres',)

    def get_genres(self, obj):
        nums = Genres.objects.all().order_by('genre_name').values('genre_id','genre_name')
        return  nums


class PreferenceAgeSerializer(serializers.ModelSerializer):
    ages = serializers.SerializerMethodField()
    class Meta:
        model = User_Preferences_Age
        fields = ('ages',)

    def get_ages(self, obj):
        return User_Preferences_Age.objects.all().values('age_low', 'age_high')

    def create(self, validated_data):
        age =  User_Preferences_Age.objects.create(**validated_data)
        return age


class PreferenceDistanceSerializer(serializers.ModelSerializer):
    distances = serializers.SerializerMethodField()
    class Meta:
        model = User_Preferences_Distance
        fields = ('distances',)

    def get_distances(self, obj):
        return User_Preferences_Distance.objects.all().values('distance_low','distance_high')

    def create(self, validated_data):
        distance =  User_Preferences_Distance.objects.create(**validated_data)
        return distance


class PreferenceGloballySerializer(serializers.ModelSerializer):
    search_globally = serializers.SerializerMethodField()
    class Meta:
        model = User_Preferences_Globally
        fields = ('search_globally',)

    def get_distances(self, obj):
        return User_Preferences_Globally.objects.all().values('search_globally')

    def create(self, validated_data):
        global_search =  User_Preferences_Globally.objects.create(**validated_data)
        return global_search


class PreferenceEditSerializer(serializers.ModelSerializer):
    
    skills = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    genders = serializers.SerializerMethodField()

    age = serializers.SerializerMethodField()


    class Meta:
        model=User
        fields=('skills', 'genres', 'genders', 'age')

    def get_skills(self, obj):
        skills = self.context.get("skills")
        return get_list_field(obj.id, "skill", skills)

    def get_genres(self, obj):
        genres = self.context.get("genres")
        return get_list_field(obj.id, "genre", genres)

    def get_genders(self, obj):
        genders = self.context.get("genders")
        return get_list_field(obj.id, "gender", genders)

    def get_age(self, obj):
        age = self.context.get("age")   # [25, 35] - ages that represent high and low
        print("This is age 147", age)
        return get_list_field(obj.id, "age", age)[0]
        # try:
        #     return get_list_field(obj.id, "age", age)[0]
        # except IndexError:
        #     print("except is in play")
        #     return list({'age_low': 5, 'age_high': 1})
    
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


        for field in Dict_Fields:
            field_name = field.value
            field_list = self.context.get(field_name)
            print("Field list:", field_list)
            if field_list is not None:
                if field_name == 'age':
                    User_Preferences_Age.objects.filter(user_id=id).delete()
                    User_Preferences_Age.objects.create(user_id=id, age_low=field_list[0], age_high=field_list[1])
                    print("User_Preferences_Age.objects.filter(user_id=id)", User_Preferences_Age.objects.filter(user_id=id))
                    # for obj in field_list:
                    #     User_Preferences_Age.objects.create(user_id=id, age_low=obj[0], age_high=obj[1])

        return instance


