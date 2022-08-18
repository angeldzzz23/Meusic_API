from rest_framework import serializers
from api.models import Image
from authentication.models import User


# TODo serializer for the image
class PictureSerialiser(serializers.ModelSerializer):
    photo_url = serializers.Serializer

    class Meta:
        model = Image
        fields = ('title', 'image')
