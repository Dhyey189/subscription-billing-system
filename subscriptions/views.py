from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from subscriptions.constants import SubscriptionStatusChoices
from subscriptions.serializers import PlanSerializer, SubscriptionSerializer
from subscriptions.models import Plan, Subscription
from rest_framework_simplejwt.authentication import JWTAuthentication


class PlanView(generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)


class SubscriptionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            kwargs["data"]["user"] = self.request.user.id

        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Subscription.objects.filter(user_id=self.request.user.id)


class SubscriptionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Subscription.objects.filter(user_id=self.request.user.id)
