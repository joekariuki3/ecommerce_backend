import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database with sample users"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Seed admin user
        admin_email = os.environ.get("ADMIN_EMAIL")
        if admin_email and admin_email.strip():
            if not User.objects.filter(email=admin_email).exists():
                User.objects.create_superuser(
                    email=admin_email,
                    username=os.environ.get("ADMIN_USERNAME"),
                    password=os.environ.get("ADMIN_PASSWORD"),
                )
                self.stdout.write(self.style.SUCCESS("Admin user created."))
        else:
            self.stdout.write(
                self.style.WARNING("ADMIN_EMAIL not set. Skipping admin user creation.")
            )

        # Seed sample users
        sample_users = [
            {
                "email": os.environ.get("USER1_EMAIL"),
                "username": os.environ.get("USER1_USERNAME"),
                "password": os.environ.get("USER1_PASSWORD"),
            },
            {
                "email": os.environ.get("USER2_EMAIL"),
                "username": os.environ.get("USER2_USERNAME"),
                "password": os.environ.get("USER2_PASSWORD"),
            },
        ]
        for u in sample_users:
            if u["email"] and u["email"].strip():
                if not User.objects.filter(email=u["email"]).exists():
                    User.objects.create_user(**u)
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "One of the USER_EMAILs is not set. Skipping that user creation."
                    )
                )

        self.stdout.write(self.style.SUCCESS("Sample users created."))

        self.stdout.write(self.style.SUCCESS("Sample data seeded."))
