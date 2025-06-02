from rest_framework.routers import DefaultRouter

from apps.api.v1.payment_plan.views.customer import CustomerPaymentPlanView
from apps.api.v1.payment_plan.views.merchant import MerchantPaymentPlanView

customer_payment_plan_router = DefaultRouter()
customer_payment_plan_router.register(
    r'',
    CustomerPaymentPlanView,
    basename='customer-payment-plan',
)

merchant_payment_plan_router = DefaultRouter()
merchant_payment_plan_router.register(
    r'',
    MerchantPaymentPlanView,
    basename='merchant-payment-plan',
)
