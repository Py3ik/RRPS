from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.refunds.models import RefundRequest
from django.core.mail import send_mail
from decouple import config


def send_notification_email(
    subject, message, recipient_list, from_email=None, fail_silently=False, **kwargs
):
    if from_email is None:
        from_email = config("DEFAULT_FROM_EMAIL", default="refund@gmail.com")

    try:
        num_sent = send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=fail_silently,
            **kwargs,
        )
        return num_sent
    except Exception as e:
        if not fail_silently:
            raise
        return 0


@receiver(pre_save, sender=RefundRequest)
def refund_status_changed(sender, instance, **kwargs):
    print("2131239812398120938102983890123")
    if instance.pk:
        old_instance = RefundRequest.objects.get(pk=instance.pk)
        recipient = instance.email or instance.user.email
        if (old_instance.status != instance.status) and recipient:
            send_notification_email(
                subject="Updating the status",
                message=f"The status of your refund on order #{instance.order_number} has been changed to {instance.status}",
                recipient_list=[recipient],
            )
