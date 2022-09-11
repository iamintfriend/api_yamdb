from rest_framework import permissions


def get_user_role(request):
    """Функция возвращает роль текущего пользователя или False для анонима."""
    if request.user.is_authenticated:
        return request.user.role

    return False


class IsAdminOrSuperuser(permissions.BasePermission):
    """У пользователя есть роль admin или он суперпользователь."""

    def has_permission(self, request, view):
        return request.user.is_superuser or get_user_role(request) == 'admin'


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Администратору и суперпользователю можно редактировать.
    Анониму только смотреть.
    Используется для моделей Categories, Genres, Titles.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser or get_user_role(request) == 'admin':
            return True


class IsOwnerStaffEditAuthPostOrReadOnly(permissions.BasePermission):
    """
    Автору объекта, админу, модератору, СП можно редактировать.
    Залогиненому пользователю можно делать POST запрос.
    Анониму только смотреть.
    Используется для моделей Reviews и Comments.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser or (
                get_user_role(request) in ('moderator', 'admin')):
            return True

        if request.user == obj.author:
            return True
