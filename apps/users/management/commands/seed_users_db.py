from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.catalog.models import Category, Product

class Command(BaseCommand):
    help = "Seed the database with sample users"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        # Seed admin user
        admin_email = "admin@example.com"
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                username="admin",
                password="adminpass"
            )
            self.stdout.write(self.style.SUCCESS("Admin user created."))

        # Seed sample users
        sample_users = [
            {"email": "user1@example.com", "username": "user1", "password": "userpass1"},
            {"email": "user2@example.com", "username": "user2", "password": "userpass2"},
        ]
        for u in sample_users:
            if not User.objects.filter(email=u["email"]).exists():
                User.objects.create_user(**u)
        self.stdout.write(self.style.SUCCESS("Sample users created."))

        self.stdout.write(self.style.SUCCESS("Sample data seeded."))