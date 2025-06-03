from rest_framework import serializers

from apps.api.v1.payment_plan.serializers import PaymentPlanSerializer
from apps.installment.models import Installments


class InstallmentSerializer(serializers.ModelSerializer):
    payment_plan = PaymentPlanSerializer()

    class Meta:
        model = Installments
        fields = '__all__'


class InstallmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installments
        fields = (
            'status',
            'paid_date',
        )


class NumericalAnalyticsSerializer(serializers.Serializer):
    total_number = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid_number = serializers.IntegerField()
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_number = serializers.IntegerField()
    pending_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    overdue_number = serializers.IntegerField()
    overdue_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class DateAnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField()
    paid_number = serializers.IntegerField()
    paid_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class InstallmentAnalyticsSerializer(serializers.Serializer):
    numerical_analytics = NumericalAnalyticsSerializer()
    date_analytics = DateAnalyticsSerializer()
    upcoming_installments = InstallmentSerializer(many=True)
