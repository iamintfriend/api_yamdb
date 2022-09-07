from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Comment, Review
from .serializers import CommentSerializer, ReviewSerializer


class ReviewSerializer(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly, )

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )
