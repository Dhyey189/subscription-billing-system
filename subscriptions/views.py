import stripe
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from subscriptions.serializers import (
    InvoiceSerializer,
    PlanSerializer,
    SubscriptionSerializer,
)
from subscriptions.models import Invoice, Plan, Subscription
from rest_framework import viewsets, mixins
from subscriptions.permissions import IsUserSubscriptionOrInvoice
from django.conf import settings


class PlanView(generics.ListAPIView):
    """
    Open API to list all active plans in the system.
    """

    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    View to handle CRUD on subscriptions model, including subscribing and unsubscribing.
    """

    permission_classes = [IsAuthenticated, IsUserSubscriptionOrInvoice]
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def get_queryset(self):
        return Subscription.objects.filter(user_id=self.request.user.id)


class InvoiceViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Handles Listing of invoices and detail view along with payment status.
    """

    permission_classes = [IsAuthenticated, IsUserSubscriptionOrInvoice]
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def get_queryset(self):
        return Invoice.objects.filter(user_id=self.request.user.id)


class InvoicePaymentView(generics.RetrieveAPIView):
    """
    APIEndpoint to send invoice's payment client_secret so that front-end can initiate payment.
    """

    permission_classes = [IsAuthenticated, IsUserSubscriptionOrInvoice]
    lookup_field = "id"

    def get_queryset(self):
        return Invoice.objects.filter(user_id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        invoice = self.get_object()

        if not invoice.stripe_payment_intent:
            return Response(
                {"detail": "Payment not initialized."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment_intent = stripe.PaymentIntent.retrieve(invoice.stripe_payment_intent)
        if not invoice.stripe_payment_intent:
            return Response(
                {"detail": "Payment not initialized."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"client_secret": payment_intent.client_secret})


class StripeWebhookView(generics.CreateAPIView):
    """
    A stripe webhook to trigger invoice status update.
    """

    def create(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.headers["STRIPE_SIGNATURE"]

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_KEY
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "payment_intent.succeeded":
            intent = event["data"]["object"]
            invoice_id = intent["metadata"].get("invoice_id")
            Invoice.objects.filter(id=invoice_id).update(status="paid")
        elif event["type"] == "payment_intent.payment_failed":
            intent = event["data"]["object"]
            invoice_id = intent["metadata"].get("invoice_id")
            Invoice.objects.filter(id=invoice_id).update(status="pending")

        return Response(status=200)
