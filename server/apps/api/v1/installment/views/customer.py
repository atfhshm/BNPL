from django.db.models import Count, Q, Sum
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api.v1.installment.serializers import (
    InstallmentAnalyticsSerializer,
    InstallmentSerializer,
)
from apps.installment.models import Installments
from bnpl.pagination import PagePaginator
from bnpl.permissions import IsCustomer
from bnpl.serializers import DetailSerializer


class CustomerInstallmentView(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    queryset = Installments.objects.all()
    serializer_class = InstallmentSerializer
    pagination_class = PagePaginator
    permission_classes = (IsAuthenticated, IsCustomer)
    http_method_names = ('get', 'post', 'delete', 'patch')

    def get_queryset(self):
        return (
            self.queryset.select_related(
                'payment_plan__merchant',
                'payment_plan__customer',
            )
            .filter(payment_plan__customer=self.request.user)
            .order_by('-due_date', '-id')
        )

    @extend_schema(
        tags=['Customer Installments'],
        summary='List all installments',
        description='List all installments for the customer',
        responses={
            status.HTTP_200_OK: InstallmentSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Customer Installments'],
        summary='Get an installment',
        description='Get an installment for the customer',
        responses={
            status.HTTP_200_OK: InstallmentSerializer,
            status.HTTP_404_NOT_FOUND: DetailSerializer,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Customer Installments'],
        summary='Pay an installment',
        description='Pay an installment for the customer',
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_400_BAD_REQUEST: DetailSerializer,
        },
    )
    @action(detail=True, methods=['patch'], url_path='pay')
    def pay(self, request, *args, **kwargs):
        installment: Installments = self.get_object()
        if installment.status != Installments.Status.PENDING:
            return Response(
                {'detail': 'Installment is not pending'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        installment.status = Installments.Status.PAID
        installment.paid_date = timezone.now().date()
        installment.save()
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Customer Installments'],
        summary='Get analytics for the customer',
        description='Get analytics for the customer',
        responses={
            status.HTTP_200_OK: InstallmentAnalyticsSerializer,
        },
    )
    @action(detail=False, methods=['get'], url_path='analytics')
    def analytics(self, request, *args, **kwargs):
        customer = request.user
        today = timezone.now().date()

        # 1. Calculate Numerical Analytics
        installments = Installments.objects.filter(
            payment_plan__customer=customer
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

        # 2. Calculate Date Analytics for the current year
        year_start = today.replace(day=1, month=1)
        year_end = today.replace(day=31, month=12)

        date_analytics = (
            installments.filter(
                status=Installments.Status.PAID, paid_date__range=[year_start, year_end]
            )
            .values('paid_date')
            .annotate(paid_number=Count('id'), paid_amount=Sum('amount'))
            .order_by('paid_date')
        )
        print(len(date_analytics))

        # 3. Get All Upcoming Installments
        upcoming_installments = installments.filter(
            status=Installments.Status.PENDING, due_date__gte=today
        ).order_by('due_date')

        # Prepare the response data
        analytics_data = {
            'numerical_analytics': numerical_data,
            'date_analytics': date_analytics,
            'upcoming_installments': InstallmentSerializer(
                upcoming_installments, many=True, context={'request': request}
            ).data,
        }

        return Response(analytics_data, status=status.HTTP_200_OK)
