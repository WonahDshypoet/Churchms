from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Admins have full access, members have read-only.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Members can only see/update their own profile, admins can see all.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.id == request.user.id
