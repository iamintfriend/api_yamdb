from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    """Расширенная модель пользователей."""

    email = models.EmailField('Почта', unique=True)
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES, default='user', max_length=10,
    )
    bio = models.TextField('Биография', blank=True, max_length=300)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
