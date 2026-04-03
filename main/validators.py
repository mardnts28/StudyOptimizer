import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    """
    Validate whether the password contains:
    - At least 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 number
    - At least 1 special character (@$!%*?&)
    """

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Password must contain at least 8 characters."),
                code='password_too_short',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Password must contain at least 1 uppercase letter."),
                code='password_no_uppercase',
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("Password must contain at least 1 lowercase letter."),
                code='password_no_lowercase',
            )
        if not re.search(r'\d', password):
            raise ValidationError(
                _("Password must contain at least 1 number."),
                code='password_no_number',
            )
        if not re.search(r'[@$!%*?&]', password):
            raise ValidationError(
                _("Password must contain at least 1 special character (@$!%*?&)."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, "
            "1 uppercase, 1 lowercase, 1 number, and 1 special character (@$!%*?&)."
        )

from django.contrib.auth.hashers import check_password

class PasswordHistoryValidator:
    def __init__(self, history_count=3):
        self.history_count = history_count

    def validate(self, password, user=None):
        if not user or not user.pk:
            return
        from main.models import PasswordHistory
        history = PasswordHistory.objects.filter(user=user).order_by('-created_at')[:self.history_count]
        for past_pass in history:
            if check_password(password, past_pass.password_hash):
                raise ValidationError(
                    _("You cannot reuse a recently used password."),
                    code='password_reused',
                )

    def get_help_text(self):
        return _("Your password cannot be the same as your last %(history_count)s passwords.") % {'history_count': self.history_count}
