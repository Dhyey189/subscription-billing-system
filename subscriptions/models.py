from django.db import models

from subscriptions.constants import (
    PLAN_TERM_TO_DAYS_MAPPING,
    InvoiceStatusChoices,
    PlanChoices,
    PlanTermChoices,
    SubscriptionStatusChoices,
)
from django.conf import settings
from django.utils.functional import cached_property
from datetime import timedelta

from users.models import TimeStampedModel


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

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    @cached_property
    def next_billing_cycle(self):
        last_invoice = self.invoices.order_by("-issue_date").first()
        if last_invoice:
            new_start_date = last_invoice.issue_date + timedelta(
                days=PLAN_TERM_TO_DAYS_MAPPING[self.plan.plan_term]
            )
        else:
            new_start_date = self.start_date
        new_end_data = new_start_date + timedelta(
            days=PLAN_TERM_TO_DAYS_MAPPING[self.plan.plan_term] - 1
        )

        return new_start_date, new_end_data


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

    def __str__(self):
        return f"Invoice #{self.id} - {self.user.email} - {self.status}"
