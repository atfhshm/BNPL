from rest_framework.routers import DefaultRouter

from apps.api.v1.auth.views.customer import CustomerAuthView
from apps.api.v1.auth.views.merchant import MerchantAuthView

customer_auth_router = DefaultRouter()
customer_auth_router.register(r'', CustomerAuthView, basename='customer-auth')

merchant_auth_router = DefaultRouter()
merchant_auth_router.register(r'', MerchantAuthView, basename='merchant-auth')
