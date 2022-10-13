from rest_framework import serializers
from .models import TechieProfile
from accounts.serializers import UserSerializer


class TechieProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TechieProfile
        fields = ['user', 'skills', 'expectation', 'companies', 'job_location',
                  'job_type', 'public', 'available_for_offer', 'up_votes', 'socials']
