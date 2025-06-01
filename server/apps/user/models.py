from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

__all__ = [
    'User',
]


class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        CUSTOMER = 'customer', _('Customer')
        MERCHANT = 'merchant', _('Merchant')
        STAFF = 'staff', _('Staff')

    first_name = models.CharField(
        _('first name'),
        max_length=150,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        db_index=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    phone_number = PhoneNumberField(
        _('phone number'),
        db_index=True,
        unique=True,
        error_messages={
            'unique': _('A user with that phone number already exists.'),
        },
    )
    user_type = models.CharField(
        _('user type'),
        max_length=10,
        choices=UserType.choices,
        default=UserType.STAFF,
    )
    is_active = models.BooleanField(
        _('active status'),
        default=True,
        db_index=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )

    date_joined = models.DateTimeField(
        _('date_joined'),
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
        db_index=True,
    )

    @property
    def is_customer(self) -> bool:
        return self.user_type == self.UserType.CUSTOMER

    @property
    def is_merchant(self) -> bool:
        return self.user_type == self.UserType.MERCHANT

    EMAIL_FIELD: str = 'email'
    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list[str] = ['first_name', 'last_name', 'phone_number']

    objects: UserManager = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-id']
