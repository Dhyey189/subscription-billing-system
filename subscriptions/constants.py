from django.db.models import TextChoices

class PlanChoices(TextChoices):
    BASIC = "basic", "Basic"
    PRO = "pro", "Pro"
    ENTERPRISE = "enterprise", "Enterprise"

class PlanTermChoices(TextChoices):
    MONTHLY = "monthly", "Monthly"
    QUATERLY = "quaterly", "Quaterly"
    HALF_YEARLY = "half_yearly", "Half Yearly"
    YEARLY = "yearly", "Yearly"

class SubscriptionStatusChoices(TextChoices):
    ACTIVE = "active", "Active" # subscription taken and started

    INACTIVE = "inactive", "Inactive" # subscription taken but not started
    CANCELLED = "cancelled", "Cancelled" # subscription cancelled by user
    EXPIRED = "expired", "Expired" # subscription expired
    SUSPENDED = "suspended", "Suspended" # it can be due payment term violations.
    PAUSE = "pause", "Pause" # subscription paused by user

class InvoiceStatusChoices(TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
