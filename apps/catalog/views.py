from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, viewsets

from .models import Category, Product
from .paginations import ProductPagination
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    Only admin users can create, update, or delete categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "category_id",
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
        return super().list(request, *args, **kwargs)
