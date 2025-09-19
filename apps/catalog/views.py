from rest_framework import viewsets
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from .permissions import IsAdminOrReadOnly
from .paginations import ProductPagination
from rest_framework import filters


class CategoryViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing category instances."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    Supports filtering by category, ordering by price, name, and creation date, and pagination.
    """
    queryset = Product.objects.select_related("category").order_by("id")
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = ProductPagination
    filterset_fields = {
        "category__id": ["exact"],
    }
    ordering_fields = ["price", "name", "created_at"]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]