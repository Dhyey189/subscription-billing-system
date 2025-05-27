from rest_framework import serializers
from subscriptions.models import Plan


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
