from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Product

class Command(BaseCommand):
    help = "Seed the database with sample categories, and products"

    def handle(self, *args, **kwargs):
        # Seed categories
        categories = [
            {"name": "Electronics", "description": "Electronic items"},
            {"name": "Books", "description": "Various books"},
            {"name": "Clothing", "description": "Apparel and accessories"},
        ]
        category_map = {}
        for cat in categories:
            obj, _ = Category.objects.get_or_create(**cat)
            category_map[cat["name"]] = obj
        self.stdout.write(self.style.SUCCESS("Sample categories seeded."))

        # Seed products
        products = [
            {"name": "Smartphone", "description": "Latest model", "price": 699.99, "stock_quantity": 50, "category": category_map["Electronics"]},
            {"name": "Novel", "description": "Bestseller", "price": 19.99, "stock_quantity": 100, "category": category_map["Books"]},
            {"name": "T-Shirt", "description": "100% cotton", "price": 9.99, "stock_quantity": 200, "category": category_map["Clothing"]},
        ]
        for prod in products:
            Product.objects.get_or_create(**prod)
        self.stdout.write(self.style.SUCCESS("Sample products seeded."))

        self.stdout.write(self.style.SUCCESS("Sample data seeded."))