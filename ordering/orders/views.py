from django.contrib.auth.models import User

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from .models import Order
from .serializers import (
    OrderSerializer,
    TotalRevenueSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint that allows normal users to make an order and admins to get total revenue.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated], 'list': [permissions.IsAuthenticated],
        'retrieve': [permissions.IsAdminUser], 'update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser]}

    def perform_create(self, serializer=OrderSerializer):
        """set the requester as the buyer."""
        serializer.save(buyer=self.request.user)

    def create(self, request, *args, **kwargs):
        """Only normal user can create an order."""
        if request.user.is_staff:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAdminUser])
    def total_revenue(self, request):
        """admins only can get the sum of all purchased items."""
        data = {'total_revenue': Order.get_sum_purchased()}
        serializer = TotalRevenueSerializer(data)
        return Response(serializer.data)
