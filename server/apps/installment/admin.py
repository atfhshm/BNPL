from django.contrib import admin

from apps.installment.models import Installments


@admin.register(Installments)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'payment_plan',
        'amount',
        'due_date',
        'paid_date',
        'status',
    )
    list_filter = (
        'status',
        'payment_plan',
        'due_date',
        'paid_date',
    )
    search_fields = (
        'payment_plan__name',
        'payment_plan__merchant__first_name',
        'payment_plan__customer__first_name',
    )
    list_filter = (
        'status',
        'payment_plan',
        'due_date',
        'paid_date',
    )
