from rest_framework import serializers
from authentication.models import User, Nationality, User_Nationality
from api.models import Images
from api.models import Videos
from authentication.functions import List_Fields, get_list_field
from newsfeed.models import User_Matches,User_Likes

# the user
# with pictures
# the video with caption
 


class ProfileSerializer(serializers.ModelSerializer):
    # the profile pictures fo the user
    pictures = serializers.SerializerMethodField()
    # the video has the caption etc
    video = serializers.SerializerMethodField()
    # the array of natinoality of the user
    nationalities = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()

    profile_url = serializers.SerializerMethodField()


    class Meta():
        model=User
        fields=('username','first_name','last_name', 'profile_url', 'pictures', 'video', 'nationalities', 'skills', 'genres')

    def get_pictures(self, obj):
        query = Images.objects.filter(user_id=obj.id).values('image_id',
                    'url', 'title')
        return list(query) if query else None

    def get_genres(self, obj):
        genres = self.context.get("genres")
        return get_list_field(obj.id, "genre", genres)

    def get_video(self, obj):
        query = Videos.objects.filter(user_id=obj.id).values('video_id',
                    'url', 'caption')
        return list(query) if query else None

    def get_nationalities(self, obj):
        nationalities = self.context.get("nationalities")
        return get_list_field(obj.id, "nationality", nationalities)

    def get_skills(self, obj):
        skills = self.context.get("skills")
        return get_list_field(obj.id, "skill", skills)

    def get_profile_url(self, obj):
         request = self.context.get("request")
         base_url = self.context.get("base_url")
         return  base_url + 'profile/' + str(obj.username)

class NewsfeedSerializer(serializers.ModelSerializer):
    feed = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields = ('feed',)
    
    def get_feed(self,obj):
        request = self.context.get("request")
        base_url = self.context.get("base_url")
        usersThatCurrUserHasLiked = [str(like.userTwo.id) for like in User_Likes.objects.filter(userLiking=request.user)]
        usersThatCurrUserHasLiked.append(request.user.id)
        all_users = User.objects.exclude(id__in=usersThatCurrUserHasLiked).exclude(is_staff=True)

        user_objects = []

        for user in all_users:
            serializer = ProfileSerializer(user, context = {'request': request, 'base_url': base_url})
            serialized_data = serializer.data
            user_objects.append(serialized_data)


        return user_objects

 

    #     return None
