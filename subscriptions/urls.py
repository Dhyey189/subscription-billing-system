from django.urls import path
from subscriptions import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"subscriptions", views.SubscriptionViewSet)
router.register(r"invoices", views.InvoiceViewSet)

urlpatterns = [
    path("plans/", views.PlanView.as_view(), name="list_plans"),
    path(
        "invoices/<int:id>/payment/",
        views.InvoicePaymentView.as_view(),
        name="get_invoice_payment_intent",
    ),
    path("stripe/webhook/", views.StripeWebhookView.as_view(), name="stripe_webhook"),
]
urlpatterns += router.urls
