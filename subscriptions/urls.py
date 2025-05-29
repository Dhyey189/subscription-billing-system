from django.urls import path
from subscriptions import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"subscriptions", views.SubscriptionViewSet)
router.register(r"invoices", views.InvoiceViewSet)

urlpatterns = [
    path("plans/", views.PlanView.as_view(), name="list_plans"),
]
urlpatterns += router.urls
