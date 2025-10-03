import logging
from io import BytesIO

from django.core.files.base import ContentFile
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from PIL import Image
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product
from .paginations import ProductPagination
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    Only admin users can create, update, or delete categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info(f"Category created: {serializer.data.get('name')}")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        logger.info(f"Category updated: {serializer.data.get('name')}")

    def perform_destroy(self, instance):
        logger.info(f"Category deleted: {instance.name}")
        super().perform_destroy(instance)


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    Supports filtering by category, searching by name, and ordering by price, name, or creation date.
    Only admin users can create, update, or delete products.
    Includes image upload and management capabilities.
    """

    IMAGE_MAX_WIDTH = 800  # Max width in pixels
    IMAGE_MAX_HEIGHT = 600  # Max height in pixels
    queryset = Product.objects.select_related("category").order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductPagination
    filterset_fields = {
        "category__id": ["exact"],
    }
    ordering_fields = ["price", "name", "created_at"]
    search_fields = ["name"]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )

    def perform_create(self, serializer):
        """Handle image compression after product creation."""
        instance = serializer.save()
        if instance.image:
            self._compress_image(instance)
        logger.info(f"Product created: {serializer.data.get('name')}")

    def perform_update(self, serializer):
        """Handle image compression after product update."""
        instance = serializer.save()
        if instance.image:
            self._compress_image(instance)
        logger.info(f"Product updated: {serializer.data.get('name')}")

    def perform_destroy(self, instance):
        """Delete associated image file when product is deleted."""
        instance.delete()
        logger.info(f"Product deleted: {instance.name}")

    def _compress_image(self, instance):
        """
        Compress and resize the product image to optimize storage and performance.
        Converts image to JPEG format and resizes it maintaining aspect ratio.
        """
        if not instance.image:
            return
        try:
            image = Image.open(instance.image.path)

            # Convert to RGB if necessary
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            # Resize image maintaining aspect ratio
            if (
                image.size[0] > self.IMAGE_MAX_WIDTH
                or image.size[1] > self.IMAGE_MAX_HEIGHT
            ):
                image.thumbnail(
                    (self.IMAGE_MAX_WIDTH, self.IMAGE_MAX_HEIGHT),
                    Image.Resampling.LANCZOS,
                )

            # Save the compressed image to a BytesIO buffer
            output = BytesIO()
            image.save(output, format="JPEG", quality=85, optimize=True)
            output.seek(0)

            # Replace the image field with the new compressed image
            instance.image.save(
                instance.image.name, ContentFile(output.getvalue()), save=False
            )
            instance.save(update_fields=["image"])

            # Close the BytesIO buffer
            output.close()

        except Exception as e:
            logger.error(
                f"Error compressing image for product {instance.name}, Id: {instance.id}: {str(e)}"
            )

    @action(detail=True, methods=["delete"], permission_classes=[IsAdminOrReadOnly])
    def delete_image(self, request, pk=None):
        """Custom action to delete the product's image."""
        product = self.get_object()
        if not product.image:
            return Response(
                {"detail": "No image to delete."}, status=status.HTTP_400_BAD_REQUEST
            )
        product.image.delete(save=True)
        logger.info(f"Image deleted for product: {product.name}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "category__id",
                openapi.IN_QUERY,
                description="Filter products by category ID (exact match) (UUID).",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "ordering",
                openapi.IN_QUERY,
                description="Order products by field. Options: price, name, created_at (prefix with '-' for descending, e.g., -price).",
                type=openapi.TYPE_STRING,
                enum=["price", "name", "created_at", "-price", "-name", "-created_at"],
            ),
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search products by name (case-insensitive partial match).",
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        logger.info("Product list viewed.")
        return super().list(request, *args, **kwargs)
