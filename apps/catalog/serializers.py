from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': False, 'allow_blank': True}
        }