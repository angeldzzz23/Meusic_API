from rest_framework import serializers
from authentication.models import User, Skills, User_Skills, Genres, User_Genres
from authentication.functions import List_Fields, get_list_field
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    skills = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta():
        model=User
        fields=('username','email','password','skills','genres')

    def get_skills(self, obj):
        skills = self.context.get("skills")        
        return get_list_field(None, obj.email, "skill", skills)
    
    def get_genres(self, obj):
        genres = self.context.get("genres")        
        return get_list_field(None, obj.email, "genre", genres)

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
    genres = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=('username','email','password','skills','genres')

    def get_skills(self, obj):
        id = self.context.get("id")
        skills = self.context.get("skills")        
        return get_list_field(id, None, "skill", skills)

    def get_genres(self, obj):
        id = self.context.get("id")
        genres = self.context.get("genres")        
        return get_list_field(id, None, "genre", genres)
    
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
