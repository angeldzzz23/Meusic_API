
from rest_framework import serializers
from authentication.models import User, Nationality, User_Nationality
from api.models import Images
from api.models import Videos
from authentication.functions import List_Fields, get_list_field

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

    class Meta():
        model=User
        fields=('username','first_name','last_name', 'pictures', 'video', 'nationalities')

    def get_pictures(self, obj):
        query = Images.objects.filter(user_id=obj.id).values('image_id',
                    'url', 'title')
        return list(query) if query else None

    def get_video(self, obj):
        query = Videos.objects.filter(user_id=obj.id).values('video_id',
                    'url', 'caption')
        return list(query) if query else None

    def get_nationalities(self, obj):
        nationalities = self.context.get("nationalities")
        return get_list_field(obj.id, "nationality", nationalities)
