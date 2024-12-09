
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow all GET requests (read-only)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is an admin for other write methods
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Allow admin users full access to the object
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
        
        # Deny write permissions to non-admin users
        return False
