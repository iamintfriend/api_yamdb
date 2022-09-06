from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределённая модель пользователя"""
    bio = models.TextField(
        'Биография',
        blank=True,
    )
