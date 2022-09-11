from rest_framework import permissions


def get_user_role(user):
    """Функция возвращает роль пользователя или False для анонима."""
    if user.is_authenticated:
        return user.role
    return False


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Администратору и суперпользователю можно редактировать.
    Анониму только смотреть.
    Используется для моделей Categories, Genres, Titles.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser or get_user_role(request.user) == 'admin':
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

        # if request.method == 'POST':
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if get_user_role(request.user) == 'moderator' or get_user_role(request.user) == 'admin':
            return True

        if request.user == obj.author:
            return True
