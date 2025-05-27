from rest_framework import serializers
from subscriptions.models import Plan, Subscription
from django.utils import timezone


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
        extra_kwargs = {"status": {"read_only": True}}

    def to_internal_value(self, data):
        if "start_date" not in data:
            data["start_date"] = timezone.now().date()

        return super().to_internal_value(data)
