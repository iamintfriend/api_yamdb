from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (CurrentUserView, ObtainTokenView, RegisterUserView,
                         UserManagementViewSet)

app_name = 'users'

user_router_v1 = DefaultRouter()
user_router_v1.register('users', UserManagementViewSet)


urlpatterns = [
    path('auth/signup/', RegisterUserView.as_view()),
    path('auth/token/', ObtainTokenView.as_view()),
    path('users/me/', CurrentUserView.as_view()),
    path('', include(user_router_v1.urls)),
]
