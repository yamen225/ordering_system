from django.contrib.auth.models import User
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer, TotalRevenueSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint that allows products to be viewed or edited by admins.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated], 'list': [permissions.IsAuthenticated],
        'retrieve': [permissions.IsAdminUser], 'update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser]}

    def perform_create(self, serializer=OrderSerializer):
        serializer.save(buyer=self.request.user)

    def create(self, request, *args, **kwargs):
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
        data = {'total_revenue': Order.get_sum_purchased()}
        serializer = TotalRevenueSerializer(data)
        return Response(serializer.data)
