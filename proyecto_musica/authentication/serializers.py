from rest_framework import serializers
from authentication.models import User, Skills, User_Skills, Genres, User_Genres, User_Artists, Genders, User_Youtube, User_Vimeo, Nationality
from api.models import Images
from api.models import Videos
from authentication.functions import List_Fields, get_list_field
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    gender_name = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    artists = serializers.SerializerMethodField()
    pictures = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    youtube_vids = serializers.SerializerMethodField()
    vimeo_vids = serializers.SerializerMethodField()
    nationalities = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('username','email','first_name','last_name', 'gender',
                'gender_name','DOB','about_me', 'password','skills','genres',
                'artists','pictures', 'video', 'youtube_vids', 'vimeo_vids', 'nationalities')

    def get_gender_name(self, obj):
        gender_id = obj.gender_id
        if gender_id:
            res = Genders.objects.get(gender_id=gender_id)
            return res.gender_name

    def get_skills(self, obj):
        skills = self.context.get("skills")
        return get_list_field(obj.id, "skill", skills)

    def get_youtube_vids(self, obj):
        vids = self.context.get("youtube_vids")
        return get_list_field(obj.id, "youtube_vids", vids)

    def get_vimeo_vids(self, obj):
        vids = self.context.get("vimeo_vids")
        return get_list_field(obj.id, "vimeo_vids", vids)


    def get_genres(self, obj):
        genres = self.context.get("genres")
        return get_list_field(obj.id, "genre", genres)

    def get_artists(self, obj):
        artists = self.context.get("artists")
        return get_list_field(obj.id, "artist", artists)

    def get_pictures(self, obj):
        query = Images.objects.filter(user_id=obj.id).values('image_id',
                    'url', 'title')
        return list(query) if query else None

    def get_video(self, obj):
        query = Videos.objects.filter(user_id=obj.id).values('video_id',
                    'url', 'title')
        return list(query) if query else None

    def get_nationalities(self, obj):
        nationalities = self.context.get("nationalities")
        return get_list_field(obj.id, "nationality", nationalities)

        # TODO: Add the youtube and vimeo videos
    def create(self, validated_data):
        user =  User.objects.create_user(**validated_data)
        user_id = (User.objects.filter(email=validated_data['email']).values('id'))[0]['id']

        for list_field in List_Fields:
            field_name = list_field.value
            field_list = self.context.get(field_name)
            if field_list:
                if field_name == 'skills':
                    for obj in field_list:
                        User_Skills.objects.create(user_id=user_id, skill_id=obj)
                elif field_name == 'genres':
                    for obj in field_list:
                        User_Genres.objects.create(user_id=user_id, genre_id=obj)
                elif field_name == 'artists':
                    for obj in field_list:
                        User_Artists.objects.create(user_id=user_id, artist=obj)
                elif field_name == 'nationalities':
                    for obj in field_list:
                        User_Nationalities.objects.create(user_id=user_id, nationality_id=obj)

        return user


class EditSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    skills = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    artists = serializers.SerializerMethodField()
    gender_name = serializers.SerializerMethodField()
    youtube_vids = serializers.SerializerMethodField()
    vimeo_vids = serializers.SerializerMethodField()
    nationalities = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=('username','email','first_name','last_name','gender',
                'gender_name','DOB','about_me','password','skills','genres',
                'artists', 'youtube_vids','vimeo_vids', 'nationality')

    def get_youtube_vids(self, obj):

        vids = self.context.get("youtube_vids")
        print('dude', vids)
        return get_list_field(obj.id, "youtube_vids", vids)

    def get_vimeo_vids(self, obj):
        vids = self.context.get("vimeo_vids")
        return get_list_field(obj.id, "vimeo_vids", vids)

    def get_gender_name(self, obj):
        gender_id = obj.gender_id
        if gender_id:
            res = Genders.objects.get(gender_id=gender_id)
            return res.gender_name

    def get_skills(self, obj):
        skills = self.context.get("skills")
        return get_list_field(obj.id, "skill", skills)

    def get_genres(self, obj):
        genres = self.context.get("genres")
        return get_list_field(obj.id, "genre", genres)

    def get_artists(self, obj):
        artists = self.context.get("artists")
        return get_list_field(obj.id, "artist", artists)

    def get_nationalities(self, obj):
        nationalities = self.context.get("nationalities")
        return get_list_field(obj.id, "nationality", nationalities)

    def update(self, instance, validated_data):
        original_email = validated_data.get('email', instance.email)
        original_username = validated_data.get('username', instance.username)
        original_password = validated_data.get('password', instance.password)

        instance.email = BaseUserManager.normalize_email(original_email)
        instance.username = AbstractBaseUser.normalize_username(original_username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.DOB = validated_data.get('DOB', instance.DOB)
        instance.about_me = validated_data.get('about_me', instance.about_me)
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(original_password)

        instance.save()

        # update other fields in corresponding tables
        id = instance.id
        for field in List_Fields:
            field_name = field.value
            field_list = self.context.get(field_name)
            if field_list is not None:
                if field_name == 'skills':
                    User_Skills.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Skills.objects.create(user_id=id, skill_id=obj)
                elif field_name == 'genres':
                    User_Genres.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Genres.objects.create(user_id=id, genre_id=obj)
                elif field_name == 'artists':
                    User_Artists.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Artists.objects.create(user_id=id, artist=obj)
                elif field_name == 'youtube_vids':
                    User_Youtube.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Youtube.objects.create(user_id=id, video_id=obj)
                elif field_name == 'vimeo_vids':
                    User_Vimeo.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Vimeo.objects.create(user_id=id, video_id=obj)

                elif field_name == 'nationalities':
                    User_Nationality.objects.filter(user_id=id).delete()
                    for obj in field_list:
                        User_Nationality.objects.create(user_id=id, nationality_id=obj)



        return instance


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta():
        model=User
        fields=('id','email','password', 'username', 'token')

        read_only_fields = ['token']


# this uses a cookie to get the token for the userr
class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            jd = super().validate(attrs)

            return jd
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

# this refreshes the user's token
# however, this does not get the refresh token from the user's cookies
class WithNoCookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        ll = self.context['request']
        attrs['refresh'] = ll.data.get('refresh')
        if attrs['refresh']:
            jd = super().validate(attrs)
            return jd
        else:
            raise InvalidToken('No valid token found in body \'refresh\'')
