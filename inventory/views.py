from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Inventory, Listing
from .serializers import ProductSerializer, InventorySerializer, ListingSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Products API
    
    Endpoints:
    - GET /api/products/ - List all products
    - POST /api/products/ - Create a new product
    - GET /api/products/{sku}/ - Get product details
    - PUT /api/products/{sku}/ - Update product
    - DELETE /api/products/{sku}/ - Delete product
    - POST /api/products/{sku}/activate/ - Activate a product
    - POST /api/products/{sku}/deactivate/ - Deactivate a product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a product"""
        product = self.get_object()
        product.is_active = True
        product.save()
        return Response({'message': f'Product {product.sku} activated successfully'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a product"""
        product = self.get_object()
        product.is_active = False
        product.save()
        return Response({'message': f'Product {product.sku} deactivated successfully'})


class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Inventory API
    
    Endpoints:
    - GET /api/inventory/ - List all inventory
    - POST /api/inventory/ - Create inventory record
    - GET /api/inventory/{id}/ - Get inventory details
    - PUT /api/inventory/{id}/ - Update inventory
    - POST /api/inventory/{id}/update-stock/ - Update stock levels
    """
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Update stock levels"""
        inventory = self.get_object()
        available = request.data.get('available_quantity')
        reserved = request.data.get('reserved_quantity')
        damaged = request.data.get('damaged_quantity')
        
        if available is not None:
            inventory.available_quantity = available
        if reserved is not None:
            inventory.reserved_quantity = reserved
        if damaged is not None:
            inventory.damaged_quantity = damaged
        
        inventory.save()
        
        serializer = self.get_serializer(inventory)
        return Response(serializer.data)


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Listings API
    
    Endpoints:
    - GET /api/listings/ - List all listings
    - POST /api/listings/ - Create a listing
    - GET /api/listings/{id}/ - Get listing details
    - PUT /api/listings/{id}/ - Update listing
    - DELETE /api/listings/{id}/ - Delete listing
    - POST /api/listings/{id}/activate/ - Activate listing
    - POST /api/listings/{id}/deactivate/ - Deactivate listing
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a listing"""
        listing = self.get_object()
        listing.listing_status = 'ACTIVE'
        listing.save()
        return Response({'message': f'Listing {listing.listing_id} activated successfully'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a listing"""
        listing = self.get_object()
        listing.listing_status = 'INACTIVE'
        listing.save()
        return Response({'message': f'Listing {listing.listing_id} deactivated successfully'})
