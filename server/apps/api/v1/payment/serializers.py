from rest_framework import serializers

from apps.api.v1.user.serializers import UserSerializer
from apps.payment_plan.models import PaymentPlan
from apps.user.models import User


class PaymentPlanSerializer(serializers.ModelSerializer):
    customer = UserSerializer()
    merchant = UserSerializer()

    class Meta:
        model = PaymentPlan
        fields = '__all__'


class CreatePaymentPlanSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type=User.UserType.CUSTOMER)
    )
    merchant = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type=User.UserType.MERCHANT)
    )

    class Meta:
        model = PaymentPlan
        fields = (
            'name',
            'total_amount',
            'no_of_installments',
        )
