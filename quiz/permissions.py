from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
    """
    Allow access only to admin users (superuser or role='admin').
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            getattr(request.user, "role", "") == "admin" or request.user.is_superuser
        )

class IsStudentUserRole(BasePermission):
    """
    Allow access only to student users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, "role", "") == "student"
