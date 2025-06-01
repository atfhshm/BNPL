from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'user_type',
            'is_active',
            'last_login',
            'date_joined',
            'updated_at',
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=_('A user with that phone number already exists.'),
            ),
        ],
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
        ]


class PasswordChangeSerializer(serializers.ModelSerializer):
    """Change password serializer"""

    password = serializers.CharField(max_length=32, write_only=True)
    new_password = serializers.CharField(max_length=32)
    confirm_new_password = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = ('password', 'new_password', 'confirm_new_password')
        read_only_fields = ('new_password', 'confirm_new_password')

    def validate(self, attrs: dict):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                detail={'new_password': ['Passwords missmatch.']},
                code=status.HTTP_400_BAD_REQUEST,
            )

        return attrs

    def validate_new_password(self, value: str):
        if value:
            validate_password(value)
        return value
