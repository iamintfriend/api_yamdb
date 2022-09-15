from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


class ConfirmationCodeGen(PasswordResetTokenGenerator):
    """
    Класс генератора кода подтверждения.
    Переопределена переменная времени действия.
    CONFIRMATION_CODE_TIMEOUT_DAYS
    """

    def check_token(self, user, token):
        """Проверка валидности кода для пользователя."""
        if not (user and token):
            return False

        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        if not constant_time_compare(
                self._make_token_with_timestamp(user, ts), token):
            return False

        if ((self._num_days(self._today()) - ts)
           > settings.CONFIRMATION_CODE_TIMEOUT_DAYS):
            return False

        return True


conf_code_generator = ConfirmationCodeGen()
