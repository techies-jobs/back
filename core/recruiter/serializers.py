from rest_framework import serializers

from techie.models import TechieProfile
from .models import RecruiterProfile
from accounts.serializers import UserSerializer
from techie.serializers import CompanySerializer
from accounts.models import Company, Roles


class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # companies = CompanySerializer(read_only=True, many=True)
    companies = serializers.SerializerMethodField()
    """
        Company is a model that has a 'roles' field, which has been serialized and added to the CompanySerializer, so
        to serialize a model that has a ManyToMany Field, you will need to add 'read_only' and 'many' fields to the 
        the model's Serialized object. Just like 'companies' attribute above, it is holds the Serialized obj of the 
        Company model which has about 2 different ManyToMany Fields 'votes' and 'roles'.
    """

    def get_companies(self, obj):
        # print(Company.objects.filter(creator=obj))
        # print(obj.companies.all())
        # for r in obj.companies.all():
        #     print(Roles.objects.filter(company=r), '---------')
        return CompanySerializer(Company.objects.filter(creator=obj), many=True).data

    class Meta:
        model = RecruiterProfile
        fields = ['user', 'image', 'headline_role', 'companies', 'socials', 'experience', 'country', 'my_job_location',
                  'is_completed', 'verified']
        depth = 1


class GetAllVerifiedRecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RecruiterProfile
        fields = ['user', 'image', 'headline_role', 'country', 'verified']


class TechiePoolSerializer(serializers.ModelSerializer):
    """
        Used to get all techies that reaches the techies pools.
        This will be seen by the recruiter.

        firstname, lastname, user's_location, verified, image, headline_role, job_type, up_votes.

    """
    user = UserSerializer()
    votes = serializers.SerializerMethodField()

    def get_votes(self, obj):
        return obj.up_votes.count()

    class Meta:
        model = TechieProfile
        fields = ['id', 'user', 'image', 'verified', 'headline_role', 'job_type', 'votes']
