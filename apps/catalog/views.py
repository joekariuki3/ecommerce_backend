import logging

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, viewsets

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
    """

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
        super().perform_create(serializer)
        logger.info(f"Product created: {serializer.data.get('name')}")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        logger.info(f"Product updated: {serializer.data.get('name')}")

    def perform_destroy(self, instance):
        logger.info(f"Product deleted: {instance.name}")
        super().perform_destroy(instance)

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
