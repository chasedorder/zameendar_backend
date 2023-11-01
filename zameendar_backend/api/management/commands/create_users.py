from django.core.management.base import BaseCommand

from zameendar_backend.api.models import User


class Command(BaseCommand):
    help = "Create user objects from provided email addresses"

    def add_arguments(self, parser):
        parser.add_argument("emails", nargs="+", type=str)

    def handle(self, *args, **options):
        for email in options["emails"]:
            user, created = User.objects.get_or_create(email=email, username=email)
            self.stdout.write(
                self.style.SUCCESS(f'User {user} {"created" if created else "already exists"}')
            )
