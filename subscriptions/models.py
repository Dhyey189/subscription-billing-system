from django.db import models

from subscriptions.constants import InvoiceStatusChoices, PlanChoices, PlanTermChoices, SubscriptionStatusChoices
from django.conf import settings

class Plan(models.Model):
    name = models.CharField(
        max_length=15, choices=PlanChoices.choices, default=PlanChoices.BASIC.value
    )
    plan_term = models.CharField(
        max_length=15, choices=PlanTermChoices.choices, default=PlanTermChoices.MONTHLY.value
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price in USD."
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.plan_term}"


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=SubscriptionStatusChoices.choices, default=SubscriptionStatusChoices.ACTIVE.value)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"
    
class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invoices')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=InvoiceStatusChoices.choices, default=InvoiceStatusChoices.PENDING.value)

    def __str__(self):
        return f"Invoice #{self.id} - {self.user.email} - {self.status}"
