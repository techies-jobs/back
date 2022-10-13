from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "last_login", "is_superuser", "is_staff", "is_active", "date_joined", "signup_type",
                   "login_type", "groups", "user_permissions"]
