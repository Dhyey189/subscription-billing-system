from rest_framework import permissions


class IsUserSubscriptionOrInvoice(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user_id == request.user.id:
            return True

        return False
