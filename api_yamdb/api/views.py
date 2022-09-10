from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from api.permissions import IsOwnerStaffEditAuthPostOrReadOnly, IsStaffOrReadOnly
import django_filters.rest_framework
from django.db.models import Avg

from reviews.models import Review, Title, Category, Genre
from .serializers import CommentSerializer, ReviewSerializer, CategorySerializer, GenreSerializer, TitlesSerializer
# from .permissions import smth
from api.mixins import CustomViewSet


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerStaffEditAuthPostOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerStaffEditAuthPostOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )


class CategoryViewSet(CustomViewSet):
    """Вьюсет для модели Category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,]
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(CustomViewSet):
    """Вьюсет для модели Genre"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,]
    search_fields = ("name",)
    lookup_field = "slug"


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitlesSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,]
