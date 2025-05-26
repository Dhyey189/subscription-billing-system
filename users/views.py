from rest_framework.response import Response
from rest_framework import generics
from users.models import User
from users.serializers import SignupSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
