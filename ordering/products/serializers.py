from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'is_deleted']

class NormalProductSerializer(ProductSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
