from django.contrib import admin

from .models import PaymentPlan


@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'status',
        'merchant',
        'customer',
        'no_of_installments',
        'total_amount',
        'total_collected_amount',
        'start_date',
    )
    list_filter = (
        'status',
        'merchant',
        'customer',
        'no_of_installments',
        'start_date',
    )
    search_fields = (
        'name',
        'merchant__first_name',
        'customer__first_name',
        'merchant__email',
        'customer__email',
        'merchant__phone_number',
        'customer__phone_number',
    )
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                'total_amount',
                'no_of_installments',
                'total_collected_amount',
            )
        return ()
