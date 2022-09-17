from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import validate_slug
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from users.utils import conf_code_generator
from reviews.models import Category, Comment, Genre, Review, Title


User = User = get_user_model()


class NewUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового пользователя."""

    email = serializers.EmailField()
    username = serializers.CharField(validators=[validate_slug, ])

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        """Валидатор для проверки имени пользователя."""
        if value == 'me':
            raise serializers.ValidationError(
                'Именем пользователя не может быть me!'
            )
        return value

    def validate(self, data):
        """
        Проверка комбинации имени пользователя и почты.
        Если пользователь с указанным именем и почтой есть,
        ему будет повторена отправка кода подтверждения.
        Если пользователя с укзанными имененм и почтой нет,
        он будет создан, ему будет выслан код подтверждения.
        """
        username_exists = User.objects.filter(
            username=data['username']).exists()
        email_exists = User.objects.filter(email=data['email']).exists()

        if username_exists is not email_exists:
            raise serializers.ValidationError(
                'Пользователь с таким именем или почтой уже существует!'
            )
        return data

    def create(self, validated_data):
        """
        Создание пользователя.
        Если пользователь с указанным именени и почтой существует,
        то ему генеруется и отправляется по почте новый код подтверждения.
        Если пользователя не существует, то он создается, ему генерируется
        и отправляется по почте код.
        """
        new_user, created = User.objects.get_or_create(**validated_data)
        confirmation_code = conf_code_generator.make_token(new_user)
        subject = 'Confirmation code for YaMDB.'
        message = (
            f'Hello {new_user.username},\nYou have just registered at YaMDB.\n'
            f'Here is your confirmation code: {confirmation_code}\n'
            'Please use it for obtaining token.\n\n'
            'Best Regards,\nYaMDB Admins'
        )
        send_mail(
            subject, message, 'yamdb@admin.com',
            [new_user.email], fail_silently=False,
        )

        return new_user


class TokenRequestSerializer(serializers.Serializer):
    """Сериализатор обработки данных для получения токена."""

    username = serializers.CharField(
        allow_blank=False, validators=[validate_slug, ]
    )
    confirmation_code = serializers.CharField(
        allow_blank=False, validators=[validate_slug, ]
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей для администратора."""

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class UserInfoSerializer(serializers.ModelSerializer):
    """Cериализатор для просмотра/изменения профиля активного пользователя."""

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('pub_date',)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists():
            raise serializers.ValidationError(
                'На одно произведение пользователь'
                'может оставить один отзыв!'
            )
        else:
            return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitlesReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
