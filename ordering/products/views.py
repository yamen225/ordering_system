from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product
from .serializers import (
    NormalProductSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint that allows all products to be viewed or edited by admins.
    Allow view available products for normal users
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'purchased']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super().list(request, *args, **kwargs)
        else:
            queryset = self.filter_queryset(Product.get_available_products())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = NormalProductSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = NormalProductSerializer(queryset, many=True)
            return Response(serializer.data)

    def perform_create(self, serializer=ProductSerializer):
        serializer.save(seller=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def purchased(self, request):
        if request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = self.filter_queryset(Product.get_all_purchased(user=request.user))
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
