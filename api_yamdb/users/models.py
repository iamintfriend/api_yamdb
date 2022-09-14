from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователей."""

    ROLE_CHOICES = (
        ('user', 'пользователь'),
        ('moderator', 'модератор'),
        ('admin', 'администратор'),
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
        return self.role == 'admin'

    def is_moderator(self):
        """"Функция проверки является ли пользователь модератором."""
        return self.role == 'moderator'
