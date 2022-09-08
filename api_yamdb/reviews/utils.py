from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validation(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Ошибка даты'),
            params={'value': value},
        )
