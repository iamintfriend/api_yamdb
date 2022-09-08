from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """У пользователя есть роль admin или он суперпользователь."""

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        else:
            return (request.user.is_superuser or request.user.role == 'admin')
