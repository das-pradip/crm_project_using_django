from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.conf import settings


@receiver(user_logged_in)
def send_login_email(sender, request, user, **kwargs):
    subject = "Login Alert - CRM System"
    message = f"""
Hello {user.username},

You have successfully logged in to the CRM system.

If this was not you, please contact support immediately.

Thank you,
CRM Team
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
