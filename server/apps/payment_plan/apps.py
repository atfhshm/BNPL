from django.apps import AppConfig


class PaymentPlanConfig(AppConfig):
    name = 'apps.payment_plan'
    label = 'payment_plan'

    def ready(self) -> None:
        from apps.payment_plan.receivers import create_installments  # noqa
