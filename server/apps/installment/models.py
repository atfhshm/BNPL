from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField

from apps.payment_plan.models import PaymentPlan
from bnpl.models import TimeStampedModelMixin


# Create your models here.
class Installments(TimeStampedModelMixin):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        OVERDUE = 'overdue', 'Overdue'
        CANCELLED = 'cancelled', 'Cancelled'

    payment_plan = models.ForeignKey(
        PaymentPlan,
        on_delete=models.CASCADE,
        related_name='installments',
        verbose_name=_('Payment Plan'),
    )

    amount = MoneyField(
        _('Amount'),
        max_digits=8,
        decimal_places=2,
        default_currency='SAR',
    )

    due_date = models.DateField(
        _('Due Date'),
    )

    paid_date = models.DateField(
        _('Paid Date'),
        null=True,
        blank=True,
    )

    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        db_table = 'installments'
        verbose_name = _('installment')
        verbose_name_plural = _('installments')
