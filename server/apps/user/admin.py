from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from apps.user.models import User

admin.site.register(Permission)


@admin.register(User)
class UserAdminConfig(UserAdmin):
    # pyrefly: ignore
    list_display = (
        'id',
        'email',
        'phone_number',
        'date_joined',
        'is_active',
        'is_staff',
        'is_superuser',
        'last_login',
        'user_type',
    )
    # pyrefly: ignore
    readonly_fields = [
        'date_joined',
        'updated_at',
        'last_login',
    ]
    # pyrefly: ignore
    fieldsets = (
        (
            'basic info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'password',
                    'user_type',
                )
            },
        ),
        (
            'groups and permissions',
            {
                'fields': (
                    'groups',
                    'user_permissions',
                )
            },
        ),
        (
            'user status',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (
            'important dates',
            {
                'fields': (
                    'date_joined',
                    'updated_at',
                    'last_login',
                )
            },
        ),
    )
    # pyrefly: ignore
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'password1',
                    'password2',
                    'user_type',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
    )
    # pyrefly: ignore
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'user_type',
    )
    # pyrefly: ignore
    search_fields = (
        'email',
        'phone_number',
        'first_name',
        'last_name',
    )
    # pyrefly: ignore
    filter_horizontal = [
        'groups',
        'user_permissions',
    ]
    # pyrefly: ignore
    ordering = (
        '-id',
        'email',
    )
