from django.db import models

from subscriptions.constants import (
    InvoiceStatusChoices,
    PlanChoices,
    PlanTermChoices,
    SubscriptionStatusChoices,
)
from django.conf import settings
from users.models import TimeStampedModel
from django.db.models import Q, UniqueConstraint


class Plan(TimeStampedModel):
    """
    Stores subscription plans for which user can subscribe to. Each plan has plan_term i.e
    duration of billing cycle and price associated with it.
    """

    name = models.CharField(
        max_length=15, choices=PlanChoices.choices, default=PlanChoices.BASIC.value
    )
    plan_term = models.CharField(
        max_length=15,
        choices=PlanTermChoices.choices,
        default=PlanTermChoices.MONTHLY.value,
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price in USD."
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.plan_term}"


class Subscription(TimeStampedModel):
    """
    Stores user's subscription for specific plan and its start date.
    At a time user can have only one active subscription.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="subscriptions"
    )
    start_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=SubscriptionStatusChoices.choices,
        default=SubscriptionStatusChoices.ACTIVE.value,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user"],
                condition=Q(status=SubscriptionStatusChoices.ACTIVE.value),
                name="unique_active_subscription_per_user",
            )
        ]

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"


class Invoice(TimeStampedModel):
    """
    Stores invoice details for specfic user's subscription.
    Invoices will generated using periodic tasks on first day of each billing cycle.
    It will store issue date and due date of invoice.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices"
    )
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="invoices"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=InvoiceStatusChoices.choices,
        default=InvoiceStatusChoices.PENDING.value,
    )
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.user.email} - {self.status}"
