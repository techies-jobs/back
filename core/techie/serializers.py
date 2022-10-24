from rest_framework import serializers
from .models import TechieProfile, Responsibility, Expectation, Skills, Company
from accounts.serializers import UserSerializer
from accounts.models import Roles


class ResponsibiltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = ['id', 'name']


class ExpectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expectation
        fields = ['id', 'expectation_value']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.up_votes.count()

    def get_roles(self, obj):
        return RoleSerializer(Roles.objects.filter(company=obj), many=True).data

    class Meta:
        model = Company
        fields = ['id', 'image', 'headline', 'about', 'votes', 'location', 'website', 'contact_url', 'roles']
        # Where 'roles' field is the available roles in the company


class TechieProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    responsibilities = serializers.SerializerMethodField(method_name="responsibility")
    expectations = serializers.SerializerMethodField(method_name="expectation")
    votes = serializers.SerializerMethodField()
    # companies = CompanySerializer(read_only=True, many=True)

    def responsibility(self, obj):
        return ResponsibiltySerializer(Responsibility.objects.all().filter(techie_profile=obj), many=True).data

    def expectation(self, obj):
        return ExpectationSerializer(Expectation.objects.all().filter(techie_profile=obj), many=True).data

    def get_votes(self, obj):
        return obj.up_votes.count()

    class Meta:
        model = TechieProfile
        fields = ['user', 'slug', 'skills', 'headline_role', 'companies', 'job_location', 'responsibilities', 'expectations',
                  'job_type', 'public', 'available_for_offer', 'socials', 'votes']
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
