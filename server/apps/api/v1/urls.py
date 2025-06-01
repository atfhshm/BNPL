from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.api.v1.auth.urls import (
    customer_auth_router,
    merchant_auth_router,
)

urlpatterns = [
    # path('admins/'),
    path(
        'merchants/',
        include(
            [
                path('auth/', include(merchant_auth_router.urls)),
            ]
        ),
    ),
    path(
        'customers/',
        include(
            [
                path('auth/', include(customer_auth_router.urls)),
            ]
        ),
    ),
]


urlpatterns.extend(
    [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path(
            'swagger/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger',
        ),
        path(
            'redoc/',
            SpectacularRedocView.as_view(url_name='schema'),
            name='redoc',
        ),
    ]
)
