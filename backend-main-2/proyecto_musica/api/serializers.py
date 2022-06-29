from rest_framework import serializers

#allows us to access our profiles models
from api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our apiview """
    name = serializers.CharField(max_length=10)


# adding a model serializer
class UserProfilesSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name','last_name', 'password','gender','account_created','about_me')



        # MODIFY this to add skills and
        extra_kwargs = {
        # you can only use it to create objects
        'password' : {
            'write_only': True,
            'style': {'input_type' : 'password'} # what does this do?
         },


        }

    # over writes the create user method
    def create(self, validated_data):
        """ create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    # def update(self, instance, validated_data):
    #     """Handle updating user account"""
    #     if 'password' in validated_data:
    #         password = validated_data.pop('password')
    #         instance.set_password(password)
    #
    #     return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""
    # this sets our serializer to our profileFeedItem model
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'create_on')
        extra_kwargs = {'user_profile': {'read_only' : True}}
