from rest_framework.pagination import PageNumberPagination
import os


class ProductPagination(PageNumberPagination):
    """Custom pagination class for products."""
    page_size = int(os.getenv("PAGE_SIZE", 10))
    page_size_query_param = "page_size"
    max_page_size = int(os.getenv("MAX_PAGE_SIZE", 100))