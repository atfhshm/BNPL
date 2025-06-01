from typing import Any

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http.request import HttpRequest
from django.utils import timezone

from apps.user.models import User

__all__ = ['AuthBackend']


class AuthBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest,
        login_term: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ) -> User | None:
        if not login_term or not password:
            return None
        search_expr = Q(email=login_term) | Q(phone_number=login_term)
        user: User | None = User.objects.filter(search_expr).first()

        if user and user.check_password(password):
            user.last_login = timezone.now()
            user.save()
            return user
        return None

    def get_user(self, user_id) -> User | None:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
