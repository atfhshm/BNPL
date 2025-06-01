from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.installment.models import Installments
from apps.payment_plan.models import PaymentPlan

__all__ = ['update_payment_plan']


@receiver(post_save, sender=Installments)
def update_payment_plan(
    sender: Installments,
    instance: Installments,
    created: bool,
    **kwargs,
):
    with transaction.atomic():
        if instance.status == Installments.Status.PAID:
            payment_plan = instance.payment_plan

            paid_installments = Installments.objects.filter(
                payment_plan=payment_plan, status=Installments.Status.PAID
            )

            total_collected = sum(
                installment.amount.amount for installment in paid_installments
            )

            payment_plan.total_collected_amount = total_collected

            if total_collected >= payment_plan.total_amount.amount:
                payment_plan.status = PaymentPlan.Status.COMPLETED

            payment_plan.save()
