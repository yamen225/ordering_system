from rest_framework import routers

from .views import OrderViewSet


order_router = routers.DefaultRouter()
order_router.register(r'orders', OrderViewSet)
