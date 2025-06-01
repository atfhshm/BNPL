from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from djmoney.money import Money

from apps.user.models import User
from bnpl.models import TimeStampedModelMixin


class PaymentPlan(TimeStampedModelMixin):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        OVERDUE = 'overdue', 'Overdue'

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
    )
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=255,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    merchant = models.ForeignKey(
        User,
        verbose_name=_('Merchant'),
        on_delete=models.CASCADE,
        related_name='merchant_payment_plans',
        limit_choices_to={'user_type': User.UserType.MERCHANT},
    )

    customer = models.ForeignKey(
        User,
        verbose_name=_('Customer'),
        on_delete=models.CASCADE,
        related_name='customer_payment_plans',
        limit_choices_to={
            'user_type': User.UserType.CUSTOMER,
        },
    )
    no_of_installments = models.IntegerField(
        verbose_name=_('Number of Installments'),
        validators=[
            MinValueValidator(
                1,
                message=_('Number of Installments must be greater than 1'),
            )
        ],
    )
    total_amount = MoneyField(
        _('Total Amount'),
        max_digits=8,
        decimal_places=2,
        default_currency='SAR',
        validators=[
            MinMoneyValidator(
                Money('50', 'SAR'),
            )
        ],
    )
    total_collected_amount = MoneyField(
        _('Total Collected Amount'),
        max_digits=8,
        decimal_places=2,
        default=Money('0', 'SAR'),
        validators=[
            MinMoneyValidator(Money('0', 'SAR')),
        ],
    )
    start_date = models.DateField(
        verbose_name=_('Start Date'),
    )

    class Meta:
        db_table = 'payment_plans'
        verbose_name = _('Payment Plan')
        verbose_name_plural = _('Payment Plans')
        ordering = ['-id']

    def __str__(self):
        return f'<PaymentPlan: {self.pk}:{self.name}>'
