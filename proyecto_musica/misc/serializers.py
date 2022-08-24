from authentication.models import Skills
from rest_framework import serializers


# this skill set
class SkillsSerializer(serializers.ModelSerializer):
    # skills = serializers.SerializerMethodField()

    class Meta:
        model = Skills
        fields = ('skill_id','skill_name',)



    def get_skills(self, obj):
        return Skills.objects.all().order_by('skill_name').values('skill_id','skill_name')


    def create(self, validated_data):
        skill =  Skills.objects.create(**validated_data)

        return skill

class AllSkillsSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = Skills
        fields = ('skills',)

    def get_skills(self, obj):
        print("sss")
        nums = Skills.objects.all().order_by('skill_name').values('skill_id','skill_name')
        print("s")
        return  nums
