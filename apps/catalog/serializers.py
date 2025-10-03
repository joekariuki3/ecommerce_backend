import os

from PIL import Image
from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Handles serialization and deserialization of Category instances.
    Validates that the name field is provided and not empty.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": False, "allow_blank": True},
        }


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    Handles serialization and deserialization of Product instances.
    Validates that name, price, stock_quantity, and category_id fields are provided.
    Ensures price and stock_quantity are non-negative.
    Includes image upload and validation.
    """

    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    IMAGE_FORMATS = ["JPEG", "JPG", "PNG", "WEBP"]
    MAX_IMAGE_ERROR_MSG = "Image size should not exceed 5MB."
    INVALID_IMAGE_ERROR_MSG = "Invalid image file."
    UNSUPPORTED_FORMAT_ERROR_MSG = "Unsupported image format. Use JPG, PNG, or WEBP."

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category_id",
            "stock_quantity",
            "category",
            "image",
        ]
        read_only_fields = ["id", "image_url"]
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": False, "allow_blank": True},
            "price": {"required": True, "min_value": 0},
            "stock_quantity": {"required": True, "min_value": 0},
            "category_id": {"required": True},
            "image": {"required": False},
        }

    def get_image_url(self, obj):
        """Return the full URL for the product image."""
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def validate_image(self, value):
        """Validate the uploaded image."""
        if not value:
            return value

        if value.size > self.MAX_IMAGE_SIZE:
            raise serializers.ValidationError(self.MAX_IMAGE_ERROR_MSG)
        try:
            img = Image.open(value)
            img.verify()
        except Exception:
            raise serializers.ValidationError(self.INVALID_IMAGE_ERROR_MSG)
        if img.format not in self.IMAGE_FORMATS:
            raise serializers.ValidationError(self.UNSUPPORTED_FORMAT_ERROR_MSG)
        return value

    def update(self, instance, validated_data):
        """Override update to handle image replacement."""
        # Only delete old image if a new image is being provided and it's different
        if "image" in validated_data and validated_data.get("image") and instance.image:
            new_image = validated_data["image"]
            # Only delete if we're actually replacing with a different image
            if new_image != instance.image:
                old_image_path = instance.image.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
        return super().update(instance, validated_data)
