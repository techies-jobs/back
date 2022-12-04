from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get("request") if self.context.get("request") else None

        if request and obj.image.url:
            return request.build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'image', 'user_role', 'location', 'bio']
