
from authentication.models import Skills
from authentication.models import Genres
from authentication.models import Genders

from rest_framework import serializers




class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genders
        fields = '__all__'
