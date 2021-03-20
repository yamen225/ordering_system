from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint that allows products to be viewed or edited by admins.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer=ProductSerializer):
        serializer.save(seller=self.request.user)
