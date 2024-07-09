import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def send_email_to_user(sender, instance, created, **kwargs):
    try:
        if created:
            subject = "Welcome to BookStore!"
            message = "Dear {},\n\nThank you for registering at BookStore.".format(
                instance.username
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = instance.email
            send_mail(subject, message, from_email, [to_email])
    except Exception as e:
        logger.error(f"Error sending email to {instance.username}: {e}")
