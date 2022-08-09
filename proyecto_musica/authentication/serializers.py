from rest_framework import serializers
from authentication.models import User, Skills, User_Skills
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
    '''skills = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=True,
        max_length=5
    )'''
    skills = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=('username','email','password','skills')

    def get_skills(self, obj):
        id = self.context.get("id")
        skills = self.context.get("skills")

        if skills is None:
            return None
        # TODO: check skills belong to skills, size limit 5, push to User_skills
        
        skill_names = []
        for skill in skills:
            s0 = Skills.objects.filter(skill_id=skill).values('skill_name')
            skill_names.append(s0[0]['skill_name'])

        return skill_names

    def update(self, instance, validated_data):
        original_email = validated_data.get('email', instance.email)
        original_username = validated_data.get('username', instance.username)
        original_password = validated_data.get('password', instance.password)

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
