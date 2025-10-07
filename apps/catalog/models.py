import os
from uuid import uuid4

from django.db import models


class Category(models.Model):
    """Model representing a product category."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def product_image_path(instance, filename):
    """Generate file path for product images."""
    ext = filename.split(".")[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join("products", filename)


class Product(models.Model):
    """Model representing a product in the catalog."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="products"
    )
    image = models.ImageField(
        upload_to=product_image_path,
        blank=True,
        null=True,
        help_text="Product image (max 5mb, JPG, PNG, WEBP)",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.category.name} - ${self.price} - Stock: {self.stock_quantity}"

    def delete(self, *args, **kwargs):
        """Override delete method to remove associated image file."""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
