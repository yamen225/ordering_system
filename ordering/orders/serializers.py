from accounts.models import User
from products.models import Product
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['buyer', 'product', 'amount']
        read_only_fields = ('buyer', )


class TotalRevenueSerializer(serializers.Serializer):

    total_revenue = serializers.FloatField(read_only=True)