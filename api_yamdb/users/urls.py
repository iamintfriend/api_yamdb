from django.urls import path

from api.views import (ObtainTokenView, RegisterUserView)


app_name = 'users'


urlpatterns = [
    path('auth/signup/', RegisterUserView.as_view()),
    path('auth/token/', ObtainTokenView.as_view()),
]
