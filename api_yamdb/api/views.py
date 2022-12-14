from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

from api.filters import TitleFilter
from api.mixins import CustomViewSet
from api.permissions import (IsAdminOrSuperuser,
                             IsOwnerStaffEditAuthPost,
                             IsStaffOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, NewUserSerializer,
                             ReviewSerializer, TitlesReadSerializer,
                             TitlesSerializer, TokenRequestSerializer, User,
                             UserInfoSerializer, UserSerializer)
from users.utils import conf_code_generator


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
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(
            User, username=serializer.data['username'],
        )
        conf_code = serializer.data['confirmation_code']

        if conf_code_generator.check_token(user, conf_code):
            token = str(RefreshToken.for_user(user).access_token)

            return Response({'access': token})

        return Response(
            {'denied': 'Указан неверный код.'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserManagementViewSet(viewsets.ModelViewSet):
    """Отображения для управления пользователями администратором."""

    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ("username", )
    permission_classes = (IsAdminOrSuperuser, )
    pagination_class = LimitOffsetPagination


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """Отображения отображения/обновления данных активного пользователя."""

    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerStaffEditAuthPost & IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsOwnerStaffEditAuthPost & IsAuthenticatedOrReadOnly]
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ("name",)
    lookup_field = "slug"
    pagination_class = PageNumberPagination


class GenreViewSet(CustomViewSet):
    """Вьюсет для модели Genre"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ("name",)
    lookup_field = "slug"


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.all().annotate(
        rating=Avg("reviews__score")
    ).order_by('name')
    serializer_class = TitlesSerializer
    permission_classes = (IsStaffOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer

        return TitlesSerializer
