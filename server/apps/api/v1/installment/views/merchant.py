from datetime import date

from django.db.models import Q, Sum
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api.v1.installment.serializers import (
    InstallmentAnalyticsSerializer,
    InstallmentSerializer,
)
from apps.installment.models import Installments
from bnpl.pagination import PagePaginator
from bnpl.permissions import IsMerchant
from bnpl.serializers import DetailSerializer


class MerchantInstallmentView(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    queryset = Installments.objects.all()
    serializer_class = InstallmentSerializer
    pagination_class = PagePaginator
    permission_classes = (IsAuthenticated, IsMerchant)
    http_method_names = (
        'get',
        'patch',
    )

    def get_queryset(self):
        return (
            self.queryset.select_related(
                'payment_plan__merchant',
                'payment_plan__customer',
            )
            .filter(payment_plan__merchant=self.request.user)
            .order_by('-due_date', '-id')
        )

    def perform_update(self, serializer):
        instance = self.get_object()

        if instance.status == Installments.Status.PAID:
            return Response(
                {'detail': 'Cannot update an installment that is already paid.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.validated_data.get('status') == Installments.Status.PAID:
            serializer.validated_data['paid_date'] = date.today()

        return super().perform_update(serializer)

    @extend_schema(
        tags=['Merchant Installments'],
        summary='List all installments',
        description='List all installments for the merchant',
        responses={
            status.HTTP_200_OK: InstallmentSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Merchant Installments'],
        summary='Get an installment',
        description='Get an installment for the merchant',
        responses={
            status.HTTP_200_OK: InstallmentSerializer,
            status.HTTP_404_NOT_FOUND: DetailSerializer,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Merchant Installments'],
        summary='Update an installment',
        description='Update an installment for the merchant',
        responses={
            status.HTTP_200_OK: InstallmentSerializer,
            status.HTTP_404_NOT_FOUND: DetailSerializer,
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Merchant Installments'],
        summary='Get analytics for the merchant',
        description='Get analytics for the merchant',
        responses={
            status.HTTP_200_OK: None,
        },
    )
    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request, *args, **kwargs):
        merchant = request.user
        today = timezone.now().date()

        # Numerical Analytics
        installments = Installments.objects.filter(
            payment_plan__merchant=merchant
        ).select_related('payment_plan')

        numerical_data = {
            'total_number': installments.count(),
            'total_amount': installments.aggregate(total=Sum('amount'))['total'] or 0,
            'paid_number': installments.filter(status=Installments.Status.PAID).count(),
            'paid_amount': installments.filter(
                status=Installments.Status.PAID
            ).aggregate(total=Sum('amount'))['total']
            or 0,
            'pending_number': installments.filter(
                status=Installments.Status.PENDING
            ).count(),
            'pending_amount': installments.filter(
                status=Installments.Status.PENDING
            ).aggregate(total=Sum('amount'))['total']
            or 0,
            'overdue_number': installments.filter(
                Q(status=Installments.Status.OVERDUE)
                | Q(status=Installments.Status.PENDING, due_date__lt=today)
            ).count(),
            'overdue_amount': installments.filter(
                Q(status=Installments.Status.OVERDUE)
                | Q(status=Installments.Status.PENDING, due_date__lt=today)
            ).aggregate(total=Sum('amount'))['total']
            or 0,
        }

        # Date Analytics (for the current year)
        current_year_start = today.replace(day=1, month=1)
        current_year_end = today.replace(day=31, month=12)

        date_data = {
            'date': today,
            'paid_number': installments.filter(
                status=Installments.Status.PAID,
                paid_date__range=[current_year_start, current_year_end],
            ).count(),
            'paid_amount': installments.filter(
                status=Installments.Status.PAID,
                paid_date__range=[current_year_start, current_year_end],
            ).aggregate(total=Sum('amount'))['total']
            or 0,
        }

        # Upcoming Installments
        upcoming_installments = (
            installments.select_related(
                'payment_plan__merchant',
                'payment_plan__customer',
            )
            .filter(status=Installments.Status.PENDING, due_date__gte=today)
            .order_by('-due_date')
        )

        # Prepare the response data
        analytics_data = {
            'numerical_analytics': numerical_data,
            'date_analytics': date_data,
            'upcoming_installments': InstallmentSerializer(
                upcoming_installments, many=True
            ).data,
        }

        serializer = InstallmentAnalyticsSerializer(analytics_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
