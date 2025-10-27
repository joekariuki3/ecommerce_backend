import logging
from io import BytesIO

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from PIL import Image
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Category, Product
from .paginations import ProductPagination
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer
from .services import generate_error_csv, process_category_csv

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    Only admin users can create, update, or delete categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        """
        Return the serializer class to use for the request.
        Returns an empty serializer for the 'bulk_upload' action
        to prevent drf-yasg from generating incorrect form fields.
        """
        if self.action == "bulk_upload":
            from rest_framework import serializers

            return serializers.Serializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info(f"Category created: {serializer.data.get('name')}")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        logger.info(f"Category updated: {serializer.data.get('name')}")

    def perform_destroy(self, instance):
        logger.info(f"Category deleted: {instance.name}")
        super().perform_destroy(instance)

    @action(
        detail=False,
        methods=["post"],
        url_path="bulk-upload",
        parser_classes=[MultiPartParser],
        permission_classes=[IsAdminUser],
    )
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="CSV file with 'name' and 'description' columns for bulk category creation.",
            )
        ],
        responses={
            200: openapi.Response(
                "All categories created successfully.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING),
                        "success_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "error_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "errors": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "row_number": openapi.Schema(
                                        type=openapi.TYPE_INTEGER
                                    ),
                                    "data": openapi.Schema(type=openapi.TYPE_OBJECT),
                                    "errors": openapi.Schema(type=openapi.TYPE_OBJECT),
                                },
                            ),
                        ),
                    },
                ),
            ),
            207: openapi.Response(
                "Partial success: some categories created, some failed.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING),
                        "success_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "error_count": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "errors": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "row_number": openapi.Schema(
                                        type=openapi.TYPE_INTEGER
                                    ),
                                    "data": openapi.Schema(type=openapi.TYPE_OBJECT),
                                    "errors": openapi.Schema(type=openapi.TYPE_OBJECT),
                                },
                            ),
                        ),
                    },
                ),
            ),
            400: "Bad Request (e.g., no file uploaded or all rows failed).",
        },
    )
    def bulk_upload(self, request):
        """
        Bulk create categories from a CSV file.
        The CSV must contain 'name' and 'description' columns.
        """

        if "file" not in request.data:
            return Response(
                {"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST
            )

        file_obj = request.data["file"]
        logger.info(
            f"Starting bulk category upload by user '{request.user}' from file '{file_obj.name}'."
        )

        result = process_category_csv(file_obj)

        logger.info(
            f"Bulk category upload finished. Success: {result['success_count']}, Errors: {result['error_count']}."
        )

        if result["error_count"] > 0 and result["success_count"] == 0:
            response_status = status.HTTP_400_BAD_REQUEST
        elif result["error_count"] > 0 and result["success_count"] > 0:
            response_status = status.HTTP_207_MULTI_STATUS  # Partial success
        else:
            response_status = status.HTTP_200_OK
        return Response(result, status=response_status)

    @action(
        detail=False,
        methods=["post"],
        url_path="download-errors",
        permission_classes=[IsAdminUser],
    )
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "errors": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "data": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                                    "description": openapi.Schema(
                                        type=openapi.TYPE_STRING
                                    ),
                                },
                            ),
                            "errors": openapi.Schema(type=openapi.TYPE_OBJECT),
                        },
                    ),
                    description="The list of error objects from the bulk upload response.",
                )
            },
            required=["errors"],
        ),
        responses={
            200: openapi.Response(
                "CSV file containing the rows that failed to upload.",
                headers={
                    "Content-Disposition": {
                        "description": 'attachment; filename="failed_categories.csv"',
                        "type": "string",
                    }
                },
            ),
            400: "Bad Request (e.g., missing 'errors' field).",
        },
    )
    def download_errors(self, request):
        """
        Takes a list of errors from bulk upload and returns a CSV
        file containing the failed rows for correction.
        """
        errors = request.data.get("errors")
        if not errors or not isinstance(errors, list):
            return Response(
                {"error": "The 'errors' field is required and must be a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        csv_content = generate_error_csv(errors)

        response = HttpResponse(csv_content, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="failed_categories.csv"'
        return response


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
