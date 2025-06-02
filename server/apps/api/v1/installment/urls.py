from rest_framework.routers import DefaultRouter

from apps.api.v1.installment.views.customer import CustomerInstallmentView
from apps.api.v1.installment.views.merchant import MerchantInstallmentView

merchant_installment_router = DefaultRouter()

merchant_installment_router.register(
    r'',
    MerchantInstallmentView,
    basename='merchant-installment',
)

customer_installment_router = DefaultRouter()

customer_installment_router.register(
    r'',
    CustomerInstallmentView,
    basename='customer-installment',
)
