from rest_framework import serializers

from techie.models import TechieProfile
from .models import RecruiterProfile
from accounts.serializers import UserSerializer
from techie.serializers import CompanySerializer
from accounts.models import Company, Roles
from techie.serializers import RoleSerializer

class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # companies = CompanySerializer(read_only=True, many=True)
    companies = serializers.SerializerMethodField()
    # job_location = serializers.SerializerMethodField()
    """
        Company is a model that has a 'roles' field, which has been serialized and added to the CompanySerializer, so
        to serialize a model that has a ManyToMany Field, you will need to add 'read_only' and 'many' fields to the 
        the model's Serialized object. Just like 'companies' attribute above, it is holds the Serialized obj of the 
        Company model which has about 2 different ManyToMany Fields 'votes' and 'roles'.
    """

    def get_companies(self, obj):
        return CompanySerializer(Company.objects.filter(creator=obj), many=True).data

    # def get_job_location(self, obj):
    #     return obj.my_job_location

    class Meta:
        model = RecruiterProfile
        fields = ['user', 'headline_role', 'companies', 'socials', 'experience', 'country', 'my_job_location',
                  'is_completed', 'verified']
        depth = 1


class GetAllVerifiedRecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RecruiterProfile
        fields = ['id', 'user', 'headline_role', 'country', 'is_completed', 'verified']


class TechiePoolSerializer(serializers.ModelSerializer):
    """
        Used to get all techies that reaches the requirements for a techies pools.
        This will be seen by the recruiter.

        firstname, lastname, user's_location, verified, image, headline_role, job_type, up_votes.

    """
    user = UserSerializer()
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.up_votes.count()

    class Meta:
        model = TechieProfile
        fields = ['id', 'user', 'verified', 'headline_role', 'job_type', 'votes']

class CompaniesAndRolesSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        print(obj, type(obj), obj.id)
        print(Roles.objects.get(company=obj))

        # if obj:
        #     roles = Roles.objects.filter(company_id=obj.id)
        #     print(roles)
        #     return RoleSerializer(instance=roles, many=True).data
        return None
    class Meta:
        model = Company
        fields = ["id", "name", "slug", "headline", "about", "roles",
                  "location", "verified", "is_completed"]
