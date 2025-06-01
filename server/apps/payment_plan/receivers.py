from datetime import timedelta

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.installment.models import Installments
from apps.payment_plan.models import PaymentPlan

__all__ = ['create_installments']


@receiver(post_save, sender=PaymentPlan)
def create_installments(
    sender: PaymentPlan,
    instance: PaymentPlan,
    created: bool,
    **kwargs,
):
    with transaction.atomic():
        if created:
            base_amount = instance.total_amount / instance.no_of_installments
            remaining_amount = instance.total_amount

            for i in range(instance.no_of_installments):
                if i == instance.no_of_installments - 1:
                    amount = remaining_amount
                else:
                    amount = base_amount
                    remaining_amount -= amount

                Installments.objects.create(
                    payment_plan=instance,
                    amount=amount,
                    amount_currency=instance.total_amount.currency,
                    due_date=instance.start_date + timedelta(days=30 * i),
                )
