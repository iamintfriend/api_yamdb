from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import IsAdminOrSuperuser
from users.serializers import (NewUserSerializer, TokenRequestSerializer, User,
                               UserInfoSerializer, UserSerializer,
                               conf_code_generator)


class RegisterUserView(generics.CreateAPIView):
    """Представление для регистрации нового пользователя."""

    serializer_class = NewUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        """Изменен статус-код ответа при удачном создании пользователя."""
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class ObtainTokenView(APIView):
    """Представления для получения токена."""
    serializer_class = TokenRequestSerializer

    def post(self, request, format=None):
        serializer = TokenRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.data['username']
            )
            conf_code = serializer.data['confirmation_code']

            if conf_code_generator.check_token(user, conf_code):
                token = str(RefreshToken.for_user(user).access_token)

                return Response({'access': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserManagementViewSet(viewsets.ModelViewSet):
    """Отображения для управления пользователями администратором."""

    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperuser, ]
    pagination_class = LimitOffsetPagination


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """Отображения отображения/обновления данных активного пользователя."""

    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return self.request.user
