from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework import serializers

User = get_user_model()
conf_code_generator = PasswordResetTokenGenerator()


class NewUserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового пользователя."""

    email = serializers.EmailField()
    username = serializers.CharField()

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

        if username_exists is email_exists:
            return data
        else:
            raise serializers.ValidationError(
                'Пользователь с таким именем или почтой уже существует!'
            )

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

    username = serializers.CharField(allow_blank=False)
    confirmation_code = serializers.CharField(allow_blank=False)


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
