from django.conf import settings
from django.core.mail import send_mail


def send_email_otp(email, otp):
    send_mail(
        subject="Zameendar OTP verificaion",
        message=f"OTP is {otp}",
        from_email=settings.SEND_EMAIL_FROM,
        recipient_list=[email],
    )
