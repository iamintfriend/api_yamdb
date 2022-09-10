from email.mime import base
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, GenreViewSet, TitlesViewSet, CategoryViewSet

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'categories', CategoryViewSet, basename='category'
)
router_v1.register(
    r'genres', GenreViewSet, basename='genre'
)
router_v1.register(
    r'titles', TitlesViewSet, basename='titles'
)


urlpatterns = [
    path('', include(router_v1.urls)),
]
