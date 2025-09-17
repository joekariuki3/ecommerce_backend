from rest_framework.permissions import SAFE_METHODS, BasePermission
class IsAdminOrReadOnly(BasePermission):
    """ Custom permission to only allow admins to edit objects.
"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff