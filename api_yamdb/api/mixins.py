from rest_framework import mixins, viewsets


class CustomViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Кастомный миксин с предустановленными методами"""
    pass
