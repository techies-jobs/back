from rest_framework import serializers
from .models import RecruiterProfile
from accounts.serializers import UserSerializer
from techie.serializers import CompanySerializer


class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RecruiterProfile
        fields = '__all__'
        depth = 1
