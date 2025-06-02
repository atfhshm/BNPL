from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.api.v1.installment.serializers import InstallmentSerializer
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
    http_method_names = ('get', 'post', 'delete')

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
