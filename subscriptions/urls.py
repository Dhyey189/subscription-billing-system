from django.urls import path
from subscriptions import views

urlpatterns = [
    path("plans/", views.PlanView.as_view(), name="list_plans"),
]
