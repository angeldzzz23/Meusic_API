from rest_framework import serializers
from api.models import Images, Videos
from authentication.models import User



class PicturesSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = Images
        fields = ('images',)

    def get_images(self, obj):

        user_id = (User.objects.filter(email=obj.email).values('id'))[0]['id']
        image_nums = Images.objects.filter(user_id=user_id).order_by('title').values('title','url', 'image_id', 'created_at')
        return image_nums



# TODo serializer for the image
class PictureSerialiser(serializers.ModelSerializer):
    #photo_url = serializers.Serializer
    #title = serializers.SerializerMethodField()
    class Meta:
        model = Images
        fields = ('image_id','title', 'url', 'created_at')


        # this will return the image

    # question:
        # is there any way to pass all of the that information as validated data
    def create(self, validated_data):
        # get the user, passed in the user
        user_obj = self.context.get("user")
        img = self.context.get("img")
        request = self.context.get("request")

        title2 = validated_data['title']

        # check if the user has other images
        # maybe there is a more pythonic way of doing this
        # https://stackoverflow.com/questions/34371959/django-property-update-a-model-instance
        CurrentUsrimages = Images.objects.filter(user=user_obj, title=title2)
        if len(CurrentUsrimages) == 1:
            editedimage = Images.objects.get(user=user_obj, title=title2)
            editedimage.image.delete(save=True)
            editedimage.image = img
            editedimage.save()

            url = request.build_absolute_uri(editedimage.image.url)
            newurl = str(url)
            editedimage.url = newurl
            editedimage.save()
            return editedimage
        pic = Images(user=user_obj, title=title2, image = img)
        pic.save()

        url = request.build_absolute_uri(pic.image.url)
        newurl = str(url)
        pic.url = newurl
        pic.save()

        return pic



class VideosSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    class Meta:
        model = Videos
        fields = ('videos',)

    def get_videos(self, obj):

        user_id = (User.objects.filter(email=obj.email).values('id'))[0]['id']
        video_nums = Videos.objects.filter(user_id=user_id).order_by('title').values('title','url', 'video_id', 'created_at', 'caption')
        return video_nums


class Videoerialiser(serializers.ModelSerializer):
    #photo_url = serializers.Serializer
    #title = serializers.SerializerMethodField()
    class Meta:
        model = Videos
        fields = ('video_id','url','caption', 'created_at')

    # question:
        # is there any way to pass all of the that information as validated data
    def create(self, validated_data):
        # get the user, passed in the user
        user_obj = self.context.get("user")
        videooo = self.context.get("vid")
        request = self.context.get("request")
        caption = self.context.get("caption")
 


        title2 = "pitch_vid"

        # check if the user has other images
        # maybe there is a more pythonic way of doing this
        # https://stackoverflow.com/questions/34371959/django-property-update-a-model-instance
        currentUsrVideo = Videos.objects.filter(user=user_obj, title=title2)
        if len(currentUsrVideo) == 1:
            editedVideo = Videos.objects.get(user=user_obj, title=title2)
            editedVideo.video.delete(save=True)
            editedVideo.video = videooo
            editedVideo.save()

            url = request.build_absolute_uri(editedVideo.video.url)
            newurl = str(url)
            editedVideo.url = newurl
            editedVideo.caption = caption
            editedVideo.save()
            return editedVideo

        newVid = Videos(user=user_obj, title=title2, video = videooo, caption=caption)
        newVid.save()

        url = request.build_absolute_uri(newVid.video.url)
        newurl = str(url)
        newVid.url = newurl
        newVid.save()

        return newVid
