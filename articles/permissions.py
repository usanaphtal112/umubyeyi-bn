from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Authenticated users only can see list view
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a post
        return obj.author == request.user


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to delete articles.
    """

    def has_permission(self, request, view):
        # Allow read-only permissions for all requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is an admin
        return request.user.is_authenticated and request.user.role.name == "Admin"


class IsAdminOrHealthAdvisorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow create, update, and delete for Admin and Health Advisor,
    and read-only permissions for all other users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            try:
                role_name = request.user.role.name
                return role_name in ["Admin", "Health Advisor"]
            except AttributeError:
                raise PermissionDenied("User role not found.")

        return False

    def has_object_permission(self, request, view, obj):
        # Allow read permissions for all requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow editing or deletion if the user is the creator of the post
        if obj.author == request.user:
            return True
        else:
            raise PermissionDenied("You are not the author of this post.")
