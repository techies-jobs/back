from rest_framework import serializers
from .models import RecruiterProfile
from accounts.serializers import UserSerializer
from techie.serializers import CompanySerializer


class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    companies = CompanySerializer(read_only=True, many=True)
    """
        Company is a model that has a 'roles' field, which has been serialized and added to the CompanySerializer, so
        to serialize a model that has a ManyToMany Field, you will need to add 'read_only' and 'many' fields to the 
        the model's Serialized object. Just like 'companies' attribute above, it is holds the Serialized obj of the 
        Company model which has about 2 different ManyToMany Fields 'votes' and 'roles'.
    """

    class Meta:
        model = RecruiterProfile
        fields = ['user', 'image', 'headline_role', 'companies', 'socials', 'experience', 'country', 'my_job_location',
                  'is_completed', 'verified']
        depth = 1


class GetAllVerifiedRecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RecruiterProfile
        fields = ['user']
