from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'is_deleted', 'currency']

class NormalProductSerializer(ProductSerializer):

    price = serializers.FloatField(read_only=True, source='user_currency_price')

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
