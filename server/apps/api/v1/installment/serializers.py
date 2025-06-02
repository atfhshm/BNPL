from rest_framework import serializers

from apps.api.v1.payment_plan.serializers import PaymentPlanSerializer
from apps.installment.models import Installments


class InstallmentSerializer(serializers.ModelSerializer):
    payment_plan = PaymentPlanSerializer()

    class Meta:
        model = Installments
        fields = '__all__'
