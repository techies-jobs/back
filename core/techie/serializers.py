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
        fields = ['id', 'name', 'slug', 'image', 'headline', 'about', 'votes', 'location', 'website', 'contact_url', 'roles']
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
        fields = ['user', 'image', 'slug', 'skills', 'headline_role', 'companies', 'job_location', 'responsibilities', 'expectations',
                  'job_type', 'public', 'available_for_offer', 'socials', 'votes']
        depth = 1


class GetAllVerifiedTechieSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TechieProfile
        fields = ['user', 'image', 'slug', 'verified', 'headline_role']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"


class CompanySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'image', 'headline', 'about']


class CompanyPoolSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    roles_count = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.up_votes.count()

    def get_roles_count(self, obj):
        return Roles.objects.filter(company=obj).count()

    # Job can't be added because a single company can have more than 1 role available and i can't just fetch those
    # role's job_type at one to the frontend
    # def get_roles_job_type(self, obj):
    #     return Roles.objects.filter(company=obj).__str__()

    class Meta:
        model = Company
        fields = ['id', 'name', 'slug', 'image', 'headline', 'about', 'votes', 'verified', 'location', 'roles_count']
        # Where 'roles_count' field is the available roles count in the company.
