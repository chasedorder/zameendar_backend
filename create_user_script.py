import os
import sys

import django

from zameendar_backend.api.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zameendar_backend.settings.dev")
django.setup()


def create_users_from_emails(emails):
    for email in emails:
        user, created = User.objects.get_or_create(username=email, email=email)
        if created:
            print(f"User created: {user.username}")
        else:
            print(f"User already exists: {user.username}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_users.py email1 email2 ...")
    else:
        email_list = sys.argv[1:]
        create_users_from_emails(email_list)
