from django.contrib import admin
from subscriptions.models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "plan_term")