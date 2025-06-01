"""
URL configuration for bnpl project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.v1.urls')),
    path('', views.root, name='root'),
]

urlpatterns.extend(
    [
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path('silk/', include('silk.urls', namespace='silk'), name='silk'),
    ]
)
