from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, InventoryViewSet, ListingViewSet
from .soap_views import inventory_soap_application

# REST API Router
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'listings', ListingViewSet, basename='listing')

urlpatterns = [
    # REST API endpoints
    path('api/', include(router.urls)),
    
    # SOAP API endpoint
    path('soap/', inventory_soap_application),
]
