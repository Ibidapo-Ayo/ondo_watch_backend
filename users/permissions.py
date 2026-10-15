from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """
    Allow access only to active Django superusers.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_active and request.user.is_superuser
        )