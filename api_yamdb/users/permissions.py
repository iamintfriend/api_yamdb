from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """У пользователя есть роль admin или он суперпользователь."""

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        else:
            return (request.user.is_superuser or request.user.role == 'admin')
