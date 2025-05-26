from rest_framework import serializers
from users.models import User

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only":True, "min_length": 6}
        }
