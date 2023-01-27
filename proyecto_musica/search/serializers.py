
from authentication.models import Skills
from authentication.models import Genres
from authentication.models import Genders
from authentication.models import Nationality

from rest_framework import serializers


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genders
        fields = '__all__'


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'

class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'
