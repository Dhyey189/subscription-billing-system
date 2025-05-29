from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from subscriptions.constants import SubscriptionStatusChoices
from subscriptions.serializers import (
    InvoiceSerializer,
    PlanSerializer,
    SubscriptionSerializer,
)
from subscriptions.models import Invoice, Plan, Subscription
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, mixins
from subscriptions.permissions import IsUserSubscriptionOrInvoice


class PlanView(generics.ListAPIView):
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsUserSubscriptionOrInvoice]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def get_queryset(self):
        return Subscription.objects.filter(user_id=self.request.user.id)


class InvoiceViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated, IsUserSubscriptionOrInvoice]
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def get_queryset(self):
        return Invoice.objects.filter(user_id=self.request.user.id)
