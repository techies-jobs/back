from rest_framework import serializers
from .models import TechieProfile, Responsibility, Expectation, Skills, Company
from accounts.serializers import UserSerializer


class ResponsibiltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = ['id', 'name']


class ExpectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expectation
        fields = ['id', 'expectation_value']


class CompanySerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.up_votes.count()

    class Meta:
        model = Company
        fields = ['votes']


class TechieProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    responsibilities = serializers.SerializerMethodField(method_name="responsibility")
    expectations = serializers.SerializerMethodField(method_name="expectation")
    up_votes_count = serializers.SerializerMethodField()

    def responsibility(self, obj):
        return ResponsibiltySerializer(Responsibility.objects.all().filter(techie_profile=obj), many=True).data

    def expectation(self, obj):
        return ExpectationSerializer(Expectation.objects.all().filter(techie_profile=obj), many=True).data

    def get_up_votes_count(self, obj):
        return obj.up_votes.count()

    class Meta:
        model = TechieProfile
        fields = ['user', 'slug', 'skills', 'headline_role', 'companies', 'job_location', 'responsibilities', 'expectations',
                  'job_type', 'public', 'available_for_offer', 'socials', 'up_votes_count']
        depth = 1


class GetAllVerifiedTechieSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TechieProfile
        fields = ['user', 'slug', 'verified', 'headline_role']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"
