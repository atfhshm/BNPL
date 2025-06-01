from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string

if TYPE_CHECKING:  # NOQA
    from .models import User


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields: dict[str, Any],
    ) -> 'User':
        if not email:
            raise ValueError('email must be provided')
        email = self.normalize_email(email=email)

        user: 'User' = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        user_type: 'User.UserType',
        **extra_fields,
    ) -> 'User':
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(
            email=email,
            password=password,
            user_type=self.model.UserType.STAFF,
            **extra_fields,
        )

    def generate_random_password(self, length: int = 8) -> str:
        allowed_chars = (
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
        )
        return get_random_string(length, allowed_chars)
