from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer
from .models import Category
from .permissions import IsAdminOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    """ A viewset for viewing and editing category instances. """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
