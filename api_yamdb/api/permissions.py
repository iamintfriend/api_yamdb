from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """У пользователя есть роль admin или он суперпользователь."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin())
        )


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Администратору и суперпользователю можно редактировать.
    Анониму только смотреть.
    Используется для моделей Categories, Genres, Titles.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin())
        )


class IsOwnerStaffEditAuthPostOrReadOnly(permissions.BasePermission):
    """
    Автору объекта, админу, модератору, СП можно редактировать.
    Залогиненому пользователю можно делать POST запрос.
    Анониму только смотреть.
    Используется для моделей Reviews и Comments.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_moderator() or request.user.is_admin()
                or request.user == obj.author
            )
        )
