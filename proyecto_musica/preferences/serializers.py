from preferences.models import Preference_Genders, Preference_Skills, Preference_Genres, User_Preference_Genders, User_Preference_Skills, User_Preference_Genres, User_Preferences_Age
from rest_framework import serializers


class PreferenceGendersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference_Genders
        fields = ('preference_gender_id','preference_gender_name',)
    def get_genders(self, obj):
        return Preference_Genders.objects.all().order_by('preference_gender_name').values('preference_gender_id','preference_gender_name')
    def create(self, validated_data):
        gender =  Preference_Genders.objects.create(**validated_data)
        return gender


class AllPreferenceGendersSerializer(serializers.ModelSerializer):
    genders = serializers.SerializerMethodField()
    class Meta:
        model = Preference_Genders
        fields = ('genders',)
    def get_genders(self, obj):
        nums = Preference_Genders.objects.all().order_by('preference_gender_name').values('preference_gender_id','preference_gender_name')
        return  nums



class PreferenceSkillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference_Skills
        fields = ('preference_skill_id','preference_skill_name',)
    def get_skills(self, obj):
        return Preference_Skills.objects.all().order_by('preference_skill_name').values('preference_skill_id','preference_skill_name')
    def create(self, validated_data):
        skill =  Preference_Skills.objects.create(**validated_data)
        return skill
    def destroy(self,request):
        print("here")
        return {}

class AllPreferenceSkillsSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Preference_Skills
        fields = ('skills',)

    def get_skills(self, obj):

        nums = Preference_Skills.objects.all().order_by('preference_skill_name').values('preference_skill_id','preference_skill_name')

        return  nums



class PreferenceGenresSerializer(serializers.ModelSerializer):
    # skills = serializers.SerializerMethodField()

    class Meta:
        model = Preference_Genres
        fields = ('preference_genre_id','preference_genre_name',)


    def create(self, validated_data):
        genres =  Preference_Genres.objects.create(**validated_data)

        return genres


class AllPreferenceGenresSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Preference_Genres
        fields = ('genres',)

    def get_genres(self, obj):
        nums = Preference_Genres.objects.all().order_by('preference_genre_name').values('preference_genre_id','preference_genre_name')
        return  nums


class PreferenceAgeSerializer(serializers.ModelSerializer):
    preference_age_id = serializers.SerializerMethodField()

    class Meta:
        model = User_Preferences_Age
        fields = ('preference_age_id','age_low','age_high')

    def get_preference_age_id(self, obj):
        nums = User_Preferences_Age.objects.all().values('age_low','age_high')
        return  nums






