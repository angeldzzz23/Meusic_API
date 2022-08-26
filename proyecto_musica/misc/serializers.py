from authentication.models import Skills
from authentication.models import Genres
from authentication.models import Genders

from rest_framework import serializers
from misc.models import Vimeo,Spotify,Youtube


# adding the gender
#gender_id
#gender_name
class GendersSerializer(serializers.ModelSerializer):
    # skills = serializers.SerializerMethodField()

    class Meta:
        model = Genders
        fields = ('gender_id','gender_name',)

    def get_genders(self, obj):
        return Genders.objects.all().order_by('gender_name').values('gender_id','gender_name')

    def create(self, validated_data):
        gender =  Genders.objects.create(**validated_data)

        return gender


class AllGendersSerializer(serializers.ModelSerializer):
    genders = serializers.SerializerMethodField()

    class Meta:
        model = Genders
        fields = ('genders',)

    def get_genders(self, obj):

        nums = Genders.objects.all().order_by('gender_name').values('gender_id','gender_name')

        return  nums




# this skill set

class SkillsSerializer(serializers.ModelSerializer):
    # skills = serializers.SerializerMethodField()

    class Meta:
        model = Skills
        fields = ('skill_id','skill_name',)

    def get_skills(self, obj):
        return Skills.objects.all().order_by('skill_name').values('skill_id','skill_name')

    def create(self, validated_data):
        skill =  Skills.objects.create(**validated_data)

        return skill

class AllSkillsSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Skills
        fields = ('skills',)

    def get_skills(self, obj):

        nums = Skills.objects.all().order_by('skill_name').values('skill_id','skill_name')

        return  nums



class GenresSerializer(serializers.ModelSerializer):
    # skills = serializers.SerializerMethodField()

    class Meta:
        model = Genres
        fields = ('genre_id','genre_name',)


    def create(self, validated_data):
        genres =  Genres.objects.create(**validated_data)

        return genres


class AllGenresSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Genres
        fields = ('genres',)

    def get_genres(self, obj):
        nums = Genres.objects.all().order_by('genre_name').values('genre_id','genre_name')
        return  nums


# Platform serializers

class SpotifySerializer(serializers.ModelSerializer):

    class Meta:
        model = Spotify
        fields = ('spotify_id','client_id','client_secret')


class VimeoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vimeo
        fields = ('vimeo_id','client_id','client_secret')

class YoutubeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Youtube
        fields = ('youtube_id','key')
