from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import Max
from subscriptions.constants import (
    DEFAULT_PAYMENT_DUE_TERM,
    INVOICE_DUE_REMINDER_INTERVAL,
    InvoiceStatusChoices,
    SubscriptionStatusChoices,
)
from subscriptions.helpers import send_template_email
from subscriptions.models import Subscription, Invoice, PLAN_TERM_TO_DAYS_MAPPING

celery_logger = get_task_logger(__name__)


@shared_task
def task_generate_invoices():
    """
    Periodic task to generate invoices for subscriptions having billing cycle start date as
    current date, runs once per day.
    """
    celery_logger.info("Start task_generate_invoices.")

    # Get subscriptions along with last invoice's issue date
    subs = (
        Subscription.objects.filter(status=SubscriptionStatusChoices.ACTIVE.value)
        .select_related("user", "plan")
        .annotate(last_invoice_issue_date=Max("invoices__issue_date"))
    )

    invoices_to_create = []
    today_date = timezone.now().date()
    for sub in subs:
        plan_term_days = PLAN_TERM_TO_DAYS_MAPPING[sub.plan.plan_term]

        if sub.last_invoice_issue_date:
            next_billing_start_date = sub.last_invoice_issue_date + timedelta(
                days=plan_term_days
            )
        else:
            next_billing_start_date = sub.start_date

        if next_billing_start_date <= today_date:
            invoices_to_create.append(
                Invoice(
                    user_id=sub.user_id,
                    subscription_id=sub.id,
                    amount=sub.plan.price,
                    issue_date=today_date,
                    due_date=today_date + timedelta(days=DEFAULT_PAYMENT_DUE_TERM),
                    status=InvoiceStatusChoices.PENDING.value,
                )
            )

    if invoices_to_create:
        invoices_created = Invoice.objects.bulk_create(invoices_to_create)
        celery_logger.info(f"Total number of invoices created: {len(invoices_created)}")

        for invoice in invoices_created:
            subject = f"Your invoice #{invoice.id} is available"
            send_template_email(
                subject=subject,
                template_name="invoice_generated",
                context={"invoice": invoice},
                recipient=invoice.user.email,
            )

    celery_logger.info("End task_generate_invoices.")


@shared_task
def task_mark_invoices_overdue():
    """
    Periodic task to update status of pending invoices to overdue.
    """
    celery_logger.info("Start task_generate_invoices.")

    today_date = timezone.now().date()
    number_of_invoice_overdued = Invoice.objects.filter(
        due_date__lt=today_date,
        status=InvoiceStatusChoices.PENDING.value,
    ).update(status=InvoiceStatusChoices.OVERDUE.value)

    celery_logger.info(
        f"Total number of invoices marked overdue: {number_of_invoice_overdued}"
    )
    celery_logger.info("End task_generate_invoices.")


@shared_task
def task_send_invoice_reminders():
    """
    Task to send payment remider emails to user having pending invoices for thier active subscription.
    Email will be sent on every INVOICE_DUE_REMINDER_INTERVAL(current value 3) days.
    """
    celery_logger.info("Start task_send_invoice_reminders.")

    today_date = timezone.now().date()
    offsets = []
    reminder_interval = INVOICE_DUE_REMINDER_INTERVAL
    while DEFAULT_PAYMENT_DUE_TERM / reminder_interval >= 1:
        offsets.append(reminder_interval)
        reminder_interval += INVOICE_DUE_REMINDER_INTERVAL

    targets = [today_date - timedelta(days=off) for off in offsets]
    invoices = Invoice.objects.filter(
        issue_date__in=targets,
        status=InvoiceStatusChoices.PENDING.value,
        due_date__gte=today_date,
    ).select_related("user", "subscription__plan")

    for invoice in invoices:
        subject = f"Reminder: Invoice #{invoice.id} due {invoice.due_date}"
        send_template_email(
            subject=subject,
            template_name="invoice_reminder",
            context={"invoice": invoice},
            recipient=invoice.user.email,
        )

    celery_logger.info(f"Total numbers of invoice reminder sent: {invoices.count()}.")
    celery_logger.info("End task_send_invoice_reminders.")
