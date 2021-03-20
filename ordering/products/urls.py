from rest_framework import routers

from .views import ProductViewSet


product_router = routers.DefaultRouter()
product_router.register(r'products', ProductViewSet)
