from authentication.models import Skills
from authentication.models import Genres
from authentication.models import Genders
from authentication.models import User, Skills, User_Skills, Genres, User_Genres, User_Artists, Genders, User_Youtube, User_Vimeo
from authentication.functions import List_Fields, get_list_field

from rest_framework import serializers


class CSkills(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('skills',)

    def get_skills(self, obj):
        skills = self.context.get("skills")
        return get_list_field(obj.id, "skill", skills)

# seeing the genres
class CGenres(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('genres',)

    def get_genres(self, obj):
        genres = self.context.get("genres")
        return get_list_field(obj.id, "genre", genres)

# seeing the favorite artist
class CArtist(serializers.ModelSerializer):
    artists = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('artists',)

    def get_artists(self, obj):
        artists = self.context.get("artists")
        return get_list_field(obj.id, "artist", artists)

# serializer for getting the youtube videos
class CYoutubeVids(serializers.ModelSerializer):
    youtube_vids = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('youtube_vids',)

    def get_youtube_vids(self, obj):
        vids = self.context.get("youtube_vids")
        return get_list_field(obj.id, "youtube_vids", vids)


# this is the serializer to get all of the vimeo viodeos
class CVimeoVids(serializers.ModelSerializer):
    vimeo_vids = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('vimeo_vids',)

    def get_vimeo_vids(self, obj):
        vids = self.context.get("vimeo_vids")
        return get_list_field(obj.id, "vimeo_vids", vids)
