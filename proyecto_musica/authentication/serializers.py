from rest_framework import serializers
from authentication.models import User, Skills, User_Skills, Genres, User_Genres
from authentication.functions import List_Fields
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class RegisterSerializer(serializers.ModelSerializer):
    # how long we want yhr password to be
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    skills = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('username','email','password','skills','genres')

    def get_skills(self, obj):
        # TODO: add external helper function 
        user_id = (User.objects.filter(email=obj.email).values('id'))[0]['id']
        skill_nums = User_Skills.objects.filter(user_id=user_id).values('skill_id')
        
        if skill_nums:
            skill_names = []
            for ele in skill_nums:
                skill_id = ele['skill_id']
                s0 = Skills.objects.filter(skill_id=skill_id).values('skill_name')
                skill_names.append(s0[0]['skill_name'])

            return skill_names
    
    def get_genres(self, obj):
        user_id = (User.objects.filter(email=obj.email).values('id'))[0]['id']
        genre_nums = User_Genres.objects.filter(user_id=user_id).values('genre_id')
        
        if genre_nums:
            genre_names = []
            for ele in genre_nums:
                genre_id = ele['genre_id']
                s0 = Genres.objects.filter(genre_id=genre_id).values('genre_name')
                genre_names.append(s0[0]['genre_name'])

            return genre_names

    def create(self, validated_data):
        user =  User.objects.create_user(**validated_data)
        user_id = (User.objects.filter(email=validated_data['email']).values('id'))[0]['id']

        for list_field in List_Fields:
            field_name = list_field.value 
            field_list = self.context.get(field_name)

            if field_list:
                if field_name == 'skills':
                    for obj in field_list:
                        User_Skills.objects.create(user_id=user_id, skill_id=obj)
                if field_name == 'genres':
                    for obj in field_list:
                        User_Genres.objects.create(user_id=user_id, genre_id=obj)

        return user


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
