from rest_framework import serializers
from authentication.models import User, Skills


class RegisterSerializer(serializers.ModelSerializer):
    # how long we want yhr password to be
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta():
        model=User
        fields=('username','email','password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SkillsSerializer(serializers.ModelSerializer):
    '''skills = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        max_length=5
    )'''
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model=User
        fields=('username','email','password')#,'skills')
    

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta():
        model=User
        fields=('id','email','password', 'username', 'token')

        read_only_fields = ['token']
