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
        category_objs = []
        for cat in categories:
            obj, _ = Category.objects.get_or_create(**cat)
            category_objs.append(obj)
        self.stdout.write(self.style.SUCCESS("Sample categories seeded."))

        # Seed products
        products = [
            {"name": "Smartphone", "description": "Latest model", "price": 699.99, "stock_quantity": 50, "category": category_objs[0]},
            {"name": "Novel", "description": "Bestseller", "price": 19.99, "stock_quantity": 100, "category": category_objs[1]},
            {"name": "T-Shirt", "description": "100% cotton", "price": 9.99, "stock_quantity": 200, "category": category_objs[2]},
        ]
        for prod in products:
            Product.objects.get_or_create(**prod)
        self.stdout.write(self.style.SUCCESS("Sample products seeded."))

        self.stdout.write(self.style.SUCCESS("Sample data seeded."))