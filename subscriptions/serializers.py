from rest_framework import serializers
from subscriptions.constants import SubscriptionStatusChoices
from subscriptions.models import Invoice, Plan, Subscription
from django.utils import timezone
from rest_framework.settings import api_settings


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "id",
            "name",
            "plan_term",
            "description",
            "price",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "user", "plan", "start_date", "status")
        extra_kwargs = {
            "user": {"default": serializers.CurrentUserDefault()},
            "start_date": {"default": timezone.now().date()},
        }

    def validate(self, attrs):
        # Allow only one active subscription per user.
        status = attrs.get("status", SubscriptionStatusChoices.ACTIVE.value)
        user = attrs.get("user")
        if status == SubscriptionStatusChoices.ACTIVE.value:
            qs = Subscription.objects.filter(
                user=user, status=SubscriptionStatusChoices.ACTIVE.value
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    {
                        api_settings.NON_FIELD_ERRORS_KEY: "You already have an active subscription."
                    }
                )

        return attrs


class InvoiceSerializer(serializers.ModelSerializer):
    payment_status = serializers.CharField(source="status")

    class Meta:
        model = Invoice
        fields = (
            "id",
            "user",
            "subscription",
            "issue_date",
            "due_date",
            "payment_status",
        )
