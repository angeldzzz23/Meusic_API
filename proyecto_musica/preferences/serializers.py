from preferences.models import Preference_Genders, Preference_Skills, Preference_Genres, User_Preference_Genders, User_Preference_Skills, User_Preference_Genres, User_Preferences_Age, User_Preferences_Distance, User_Preferences_Globally
from authentication.models import User
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



class EditPreferenceSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    search_globally = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=('gender', 'skills', 'genres', 'age', 'distance', 'search_globally')

    def get_gender(self, obj):
        preference_gender_id = obj.preference_gender_id
        if preference_gender_id:
            res = Preference_Genders.objects.get(preference_gender_id=preference_gender_id)
            return res.preference_gender_name

    def get_skills(self, obj):
        preference_skills = self.context.get("preference_skill_name")
        return get_list_field(obj.id, "skill", preference_skills)

    def get_genres(self, obj):
        genres = self.context.get("preference_genre")
        return get_list_field(obj.id, "genre", preference_genre_name)

    def get_age(self, obj):
        preference_age = self.context.get("preference_age")
        return get_list_field(obj.id, "age", preference_age)


    def get_distance(self, obj):
        artists = self.context.get("preference_distance")
        return get_list_field(obj.id, "artist", artists)

    def update(self, instance, validated_data):
        instance.preference_gender = validated_data.get('gender', instance.preference_gender)

        instance.save()

        # update other fields in corresponding tables
        id = instance.id
        for field in List_Fields:
            field_name = field.value
            field_list = self.context.get(field_name)
            if field_list is not None:
                if field_name == 'preference_skills':
                    User_Preference_Skills.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Skills.objects.create(user_id=id, skill_id=obj)
                elif field_name == 'genres':
                    User_Preference_Genres.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Preference_Genres.objects.create(user_id=id, genre_id=obj)

        return instance







