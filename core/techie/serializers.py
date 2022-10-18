from rest_framework import serializers
from .models import TechieProfile, Responsibility, Expectation
from accounts.serializers import UserSerializer


class ResponsibiltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = ['id', 'name']


class ExpectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expectation
        fields = ['id', 'expectation_value']


class TechieProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    responsibilities = serializers.SerializerMethodField(method_name="responsibility")
    expectations = serializers.SerializerMethodField(method_name="expectation")

    def responsibility(self, obj):
        return ResponsibiltySerializer(Responsibility.objects.all().filter(techie_profile=obj), many=True).data

    def expectation(self, obj):
        return ExpectationSerializer(Expectation.objects.all().filter(techie_profile=obj), many=True).data

    class Meta:
        model = TechieProfile
        fields = ['user', 'slug', 'skills', 'headline_role', 'companies', 'job_location', 'responsibilities', 'expectations',
                  'job_type', 'public', 'available_for_offer', 'socials']
        depth = 1


class GetAllVerifiedTechieSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TechieProfile
        fields = ['user', 'slug', 'verified', 'headline_role']
