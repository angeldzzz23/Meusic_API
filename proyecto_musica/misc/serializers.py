from authentication.models import Skills
from authentication.models import Genres
from rest_framework import serializers
from misc.models import Vimeo,Spotify,Youtube



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
