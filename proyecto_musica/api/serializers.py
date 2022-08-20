from rest_framework import serializers
from api.models import Image
from authentication.models import User


# TODo serializer for the image
class PictureSerialiser(serializers.ModelSerializer):
    #photo_url = serializers.Serializer
    #title = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('image_id','title', 'url', 'created_at')


        # this will return the image

    # question:
        # is there any way to pass all of the that information as validated data
    def create(self, validated_data):
        # get the user, passed in the user
        user_obj = self.context.get("user")
        img = self.context.get("img")
        request = self.context.get("request")

        title2 = validated_data['title']

        # check if the user has other images
        # maybe there is a more pythonic way of doing this
        # https://stackoverflow.com/questions/34371959/django-property-update-a-model-instance
        CurrentUsrimages = Image.objects.filter(user=user_obj, title=title2)
        if len(CurrentUsrimages) == 1:
            editedimage = Image.objects.get(user=user_obj, title=title2)
            editedimage.image.delete(save=True)
            editedimage.image = img
            editedimage.save()

            url = request.build_absolute_uri(editedimage.image.url)
            newurl = str(url)
            editedimage.url = newurl
            editedimage.save()
            return editedimage


        pic = Image(user=user_obj, title=title2, image = img)
        pic.save()

        url = request.build_absolute_uri(pic.image.url)
        newurl = str(url)
        pic.url = newurl
        pic.save()

        return pic


'''
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
        skills = self.context.get("skills")

        # Add skills to User_Skills
        if skills:
            user_id = (User.objects.filter(email=validated_data['email']).values('id'))[0]['id']
            for skill in skills:
                User_Skills.objects.create(user_id=user_id, skill_id=skill)

        return the_user
'''
