from rest_framework import serializers
from authentication.models import User, Skills, User_Skills
from rest_framework.validators import UniqueValidator
#from authentication.functions import normalize_email
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class RegisterSerializer(serializers.ModelSerializer):
    # how long we want yhr password to be
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    skills = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('username','email','password','skills')

    def get_skills(self, obj):
        user_id = (User.objects.filter(email=obj.email).values('id'))[0]['id']
        skill_nums = User_Skills.objects.filter(user_id=user_id).values('skill_id')
        
        if skill_nums is None:
            return None

        skill_names = []
        for ele in skill_nums:
            skill_id = ele['skill_id']
            s0 = Skills.objects.filter(skill_id=skill_id).values('skill_name')
            skill_names.append(s0[0]['skill_name'])

        return skill_names

    def create(self, validated_data):
        the_user =  User.objects.create_user(**validated_data)
            
        # add to user_skills
        return the_user


class EditSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())]) 
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())]) 
    skills = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=('username','email','password','skills')

    def get_skills(self, obj):
        id = self.context.get("id")
        skills = self.context.get("skills")

        if skills is None:
            return None
        
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
