from rest_framework.permissions import BasePermission

class IsManagerOrAdmin(BasePermission):
    """
    Custom permission to only allow managers or admins to access the view.
    """

    def has_permission(self, request, view):
        # Ensure that the user has an associated userinfo
        user_info = getattr(request.user, 'userinfo', None)
        
        if user_info:
            # Check if the role is Manager or Admin
            return user_info.role in ['Manager', 'Admin']
        return False
