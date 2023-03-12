from authentication.models import Skills
from authentication.models import Genres
from authentication.models import Genders
from authentication.models import User, Skills, User_Skills, Genres, User_Genres, User_Artists, Genders, User_Youtube, User_Vimeo
from authentication.models import User_Nationality
from authentication.functions import List_Fields, get_list_field
from api.models import Videos
from api.models import Images
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

# TODO:
class CGender(serializers.ModelSerializer):
    gender_name = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('gender_name',)

    def get_gender_name(self, obj):
        gender_id = obj.gender_id
        if gender_id:
            res = Genders.objects.get(gender_id=gender_id)
            return res.gender_name


# seeing the favorite artist
class CArtist(serializers.ModelSerializer):
    artists = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('artists',)

    def get_artists(self, obj):
        artists = self.context.get("artists")
        return get_list_field(obj.id, "artist", artists)

# this serializer gets all of the videos 
class CUserVideos(serializers.ModelSerializer):
      videos = serializers.SerializerMethodField()
      
      class Meta():
        model=User
        fields=('videos',)

      def get_videos(self, obj):
        vids = self.context.get("videos")
        return get_list_field(obj.id, "videos", vids)

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


class CPersonalVideo(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('video',)

    def get_video(self, obj):
        query = Videos.objects.filter(user_id=obj.id).values('video_id',
                    'url', 'title')
        return list(query) if query else None


class CPersonalPictures(serializers.ModelSerializer):
    pictures = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('pictures',)

    def get_pictures(self, obj):
        query = Images.objects.filter(user_id=obj.id).values('image_id',
                    'url', 'title')
        return list(query) if query else None

# fields=('username','email', 'first_name', 'last_name', 'last_name','DOB', 'about_me', )



class CDOBOfUser(serializers.ModelSerializer):
    class Meta():
        model=User
        fields=('DOB',)


class CTheNameOfUser(serializers.ModelSerializer):
    class Meta():
        model=User
        fields=('first_name','last_name',)


class CusernameInfo(serializers.ModelSerializer):

    class Meta():
        model=User
        fields=('username', )


class CusernameInfo(serializers.ModelSerializer):

    class Meta():
        model=User
        fields=('username', )



class CPersonalInfo(serializers.ModelSerializer):

    class Meta():
        model=User
        fields=('about_me', )

# this is the
class Cnationalities(serializers.ModelSerializer):
    nationality = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('nationality',)

    def get_nationality(self, obj):
        nationalities = self.context.get("nationalities")
        return get_list_field(obj.id, "nationality", nationalities)
