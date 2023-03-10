from rest_framework import serializers
from authentication.models import User, Nationality, User_Nationality
from api.models import Images
from api.models import Videos
from authentication.functions import List_Fields, get_list_field


class MatchesSerializer(serializers.ModelSerializer):
    # the profile pictures fo the user
    # the video has the caption etc
    video = serializers.SerializerMethodField()

    feed_item_url = serializers.SerializerMethodField()


    class Meta():
        model=User
        fields=('username','first_name','last_name', 'feed_item_url', 'video', )

    def get_video(self, obj):
        query = Videos.objects.filter(user_id=obj.id).values('video_id',
                    'url', 'caption')
        return list(query) if query else None

    def get_feed_item_url(self, obj):
         request = self.context.get("request")
         base_url = self.context.get("base_url")


         return  base_url + 'newsfeed/user/' + obj.username
