from django.urls import path
from subscriptions import views

urlpatterns = [
    path("plans/", views.PlanView.as_view(), name="list_plans"),
    path(
        "subscriptions/", views.SubscriptionListCreateView.as_view(), name="list_create_subscription"
    ),
    path(
        "subscriptions/<int:id>/", views.SubscriptionRetrieveUpdateView.as_view(), name="get_update_subscription"
    ),
]
