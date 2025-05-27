from rest_framework.response import Response
from rest_framework import generics, status

from subscriptions.serializers import PlanSerializer
from subscriptions.models import Plan


class PlanView(generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)
