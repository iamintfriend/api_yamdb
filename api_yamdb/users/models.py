from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователей."""

    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'
    MODERATOR_ROLE = 'moderator'

    ROLE_CHOICES = (
        (USER_ROLE, 'пользователь'),
        (MODERATOR_ROLE, 'модератор'),
        (ADMIN_ROLE, 'администратор'),
    )
    email = models.EmailField('Почта', unique=True)
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES, default='user', max_length=20,
    )
    bio = models.TextField('Биография', blank=True, max_length=300)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_admin(self):
        """Функция проверки является ли пользователь админом."""
        return self.role == self.ADMIN_ROLE

    def is_moderator(self):
        """"Функция проверки является ли пользователь модератором."""
        return self.role == self.MODERATOR_ROLE
