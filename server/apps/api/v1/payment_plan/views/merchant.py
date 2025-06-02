from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.api.v1.payment_plan.serializers import (
    CreatePaymentPlanSerializer,
    PaymentPlanSerializer,
)
from apps.installment.models import Installments
from apps.payment_plan.models import PaymentPlan
from bnpl.pagination import PagePaginator
from bnpl.permissions import IsMerchant
from bnpl.serializers import get_serializer_validation_errors


class MerchantPaymentPlanView(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
):
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    pagination_class = PagePaginator
    permission_classes = (IsAuthenticated, IsMerchant)
    http_method_names = ('get', 'post', 'delete')

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePaymentPlanSerializer
        return PaymentPlanSerializer

    def get_queryset(self):
        qs = (
            self.queryset.select_related(
                'customer',
                'merchant',
            )
            .filter(merchant=self.request.user)
            .annotate(
                no_of_paid_installments=Count(
                    'installments',
                    filter=Q(installments__status=Installments.Status.PAID),
                ),
            )
            .order_by('-id')
        )
        return qs

    def perform_create(self, serializer):
        serializer.save(
            merchant=self.request.user,
            status=PaymentPlan.Status.ACTIVE,
        )

    def perform_destroy(self, instance):
        existing_installments = instance.installments.filter(
            status__in=[
                Installments.Status.PAID,
                Installments.Status.OVERDUE,
            ],
        )
        if existing_installments.exists():
            raise ValidationError(
                {
                    'detail': _(
                        'This payment plan already has paid or overdue installments'
                    ),
                }
            )
        super().perform_destroy(instance)

    @extend_schema(
        tags=['Merchant Payment Plan'],
        summary='List all payment plans for the merchant',
        description='List all payment plans for the merchant',
        responses={
            status.HTTP_200_OK: PaymentPlanSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Merchant Payment Plan'],
        summary='Get a payment plan for the merchant',
        description='Get a payment plan for the merchant',
        responses={
            status.HTTP_200_OK: PaymentPlanSerializer(),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Merchant Payment Plan'],
        summary='Create a payment plan for the merchant',
        description='Create a payment plan for the merchant',
        request=CreatePaymentPlanSerializer,
        responses={
            status.HTTP_201_CREATED: PaymentPlanSerializer(),
        },
        examples=[
            get_serializer_validation_errors(PaymentPlanSerializer),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Merchant Payment Plan'],
        summary='Delete a payment plan for the merchant',
        description='Delete a payment plan for the merchant',
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
