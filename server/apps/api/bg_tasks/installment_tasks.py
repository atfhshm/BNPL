from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils import timezone

from apps.installment.models import Installments
from bnpl.settings import DEFAULT_FROM_EMAIL


@shared_task
def check_overdue_installments():
    """
    Daily task to check and mark overdue installments.
    Runs at 12 AM every day.
    """
    today = timezone.now().date()

    # Find all pending installments where due_date is in the past
    overdue_installments = Installments.objects.filter(
        Q(status=Installments.Status.PENDING) | Q(status=Installments.Status.ACTIVE),
        due_date__lt=today,
    )

    # Update status to OVERDUE
    overdue_installments.update(status=Installments.Status.OVERDUE)

    # Send email notifications for overdue installments
    for installment in overdue_installments:
        customer = installment.payment_plan.customer
        context = {
            'customer_name': customer.first_name,
            'amount': installment.amount,
            'due_date': installment.due_date,
            'payment_plan_name': installment.payment_plan.name,
        }

        # Render email content
        html_message = render_to_string('emails/overdue_installment.html', context)

        # Send email
        send_mail(
            subject='Installment Overdue Notice',
            message=f'Your installment of {installment.amount} for payment plan {installment.payment_plan.name} is overdue.',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[customer.email],
            html_message=html_message,
            fail_silently=False,
        )


@shared_task
def send_installment_reminders():
    """
    Daily task to send reminders for upcoming installments.
    Sends reminders 3 days before the due date.
    """
    today = timezone.now().date()
    reminder_date = today + timedelta(days=3)

    # Find all pending installments due in 3 days
    upcoming_installments = Installments.objects.filter(
        Q(status=Installments.Status.PENDING) | Q(status=Installments.Status.ACTIVE),
        due_date=reminder_date,
    )

    # Send reminder emails
    for installment in upcoming_installments:
        customer = installment.payment_plan.customer
        context = {
            'customer_name': customer.first_name,
            'amount': installment.amount,
            'due_date': installment.due_date,
            'payment_plan_name': installment.payment_plan.name,
        }

        # Render email content
        html_message = render_to_string('emails/installment_reminder.html', context)

        # Send email
        send_mail(
            subject='Upcoming Installment Reminder',
            message=f'Your installment of {installment.amount} for payment plan {installment.payment_plan.name} is due in 3 days.',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[customer.email],
            html_message=html_message,
            fail_silently=False,
        )
