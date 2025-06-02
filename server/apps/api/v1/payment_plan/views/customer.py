from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.api.v1.payment_plan.serializers import PaymentPlanSerializer
from apps.installment.models import Installments
from apps.payment_plan.models import PaymentPlan
from bnpl.pagination import PagePaginator
from bnpl.permissions import IsCustomer


class CustomerPaymentPlanView(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    pagination_class = PagePaginator
    permission_classes = (IsAuthenticated, IsCustomer)
    http_method_names = ('get', 'patch')

    def get_queryset(self):
        qs = (
            self.queryset.select_related(
                'customer',
                'merchant',
            )
            .filter(customer=self.request.user)
            .annotate(
                no_of_paid_installments=Count(
                    'installments',
                    filter=Q(installments__status=Installments.Status.PAID),
                ),
            )
            .order_by('-id')
        )
        return qs

    @extend_schema(
        tags=['Customer Payment Plan'],
        summary='List all payment plans for the customer',
        description='List all payment plans for the customer',
        responses={
            status.HTTP_200_OK: PaymentPlanSerializer(many=True),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Customer Payment Plan'],
        summary='Get a payment plan for the customer',
        description='Get a payment plan for the customer',
        responses={
            status.HTTP_200_OK: PaymentPlanSerializer(),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
