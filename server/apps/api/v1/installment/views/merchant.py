from datetime import date

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api.v1.installment.serializers import InstallmentSerializer
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
