from rest_framework.routers import DefaultRouter

from apps.api.v1.user.views.customer import CustomerView
from apps.api.v1.user.views.merchant import MerchantView

customer_router = DefaultRouter()
customer_router.register(r'', CustomerView, basename='customers')
merchant_router = DefaultRouter()
merchant_router.register(r'', MerchantView, basename='merchant-users')
