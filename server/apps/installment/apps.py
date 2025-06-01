from django.apps import AppConfig


class InstallmentConfig(AppConfig):
    name = 'apps.installment'
    label = 'installment'

    def ready(self) -> None:
        from apps.installment.receivers import update_payment_plan  # noqa
