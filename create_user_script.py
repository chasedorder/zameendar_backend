import os

import django

from zameendar_backend.api.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zameendar_backend.settings.dev")
django.setup()


def create_user_from_emails(emails):
    for email in emails:
        user, created = User.objects.get_or_create(username=email, email=email)
        if created:
            print(f"User created: {user.username}")
        else:
            print(f"User already exists: {user.username}")


if __name__ == "__main__":
    email_list = list(map(str.strip, input().split(",")))
    create_user_from_emails(email_list)
