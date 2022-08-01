from rest_framework import serializers
from authentication.models import User, Skills
from rest_framework.validators import UniqueValidator
#from authentication.functions import normalize_email
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class RegisterSerializer(serializers.ModelSerializer):
    # how long we want yhr password to be
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta():
        model=User
        fields=('username','email','password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SkillsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())]) 
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())]) 

    class Meta:
        model=User
        fields=('username','email','password')#,'skills')

    def update(self, instance, validated_data):
        original_email = validated_data.get('email', instance.email)
        original_username = validated_data.get('username', instance.username)
        original_password = validated_data.get('password', instance.password)
        
        # get id
        #print(self.context.get("id"))

        instance.email = BaseUserManager.normalize_email(original_email)
        instance.username = AbstractBaseUser.normalize_username(original_username)
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(original_password)
        
        instance.save()
        
        return instance


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta():
        model=User
        fields=('id','email','password', 'username', 'token')

        read_only_fields = ['token']
