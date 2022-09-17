from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validation(value):
    """Проверка на существующую дату"""
    if value > timezone.now().year:
        raise ValidationError(
            ('Недопустимая дата: дата не может быть больше сегодняшнего дня'),
            params={'value': value},
        )
