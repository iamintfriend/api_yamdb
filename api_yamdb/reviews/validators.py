from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validation(value):
    """Проверка на существующую дату"""
    if value > timezone.now().year:
        raise ValidationError(
            ('Несуществующая дата'),
            params={'value': value},
        )


def score_validation(value):
    """Проверка на существующий балл"""
    if value > 10:
        raise ValidationError(
            ("Балл не может быть выше 10"),
            params={'value': value},
        )
