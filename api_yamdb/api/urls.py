from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, CurrentUserView,
                    GenreViewSet, ObtainTokenView, RegisterUserView,
                    ReviewViewSet, TitlesViewSet, UserManagementViewSet)


router_v1 = DefaultRouter()
router_v1.register('users', UserManagementViewSet)
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
    path('auth/signup/', RegisterUserView.as_view()),
    path('auth/token/', ObtainTokenView.as_view()),
    path('users/me/', CurrentUserView.as_view()),
    path('', include(router_v1.urls)),
]
