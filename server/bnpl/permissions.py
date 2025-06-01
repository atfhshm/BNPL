from rest_framework.permissions import BasePermission

__all__ = [
    'IsStaff',
    'IsCustomer',
    'IsMerchant',
]


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer


class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_merchant
