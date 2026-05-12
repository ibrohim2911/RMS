from rest_framework import permissions
class HasDynamicPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 1. Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 2. Get the required permission from the view
        required_perm = getattr(view, 'required_permission', None)
        if not required_perm:
            return True # If no permission is set on the view, allow access
            
        # 3. Check if the user's role has this permission
        return request.user.role.permissions.filter(slug=required_perm).exists()