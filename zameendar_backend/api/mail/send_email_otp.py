from django.conf import settings
from django.core.mail import send_mail


def send_email_otp(email, otp):
    send_mail(
        subject="Zameendar OTP verificaion",
        message=f"OTP is {otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
