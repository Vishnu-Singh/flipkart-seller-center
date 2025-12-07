from rest_framework import serializers
from .models import Product, Inventory, Listing


class InventorySerializer(serializers.ModelSerializer):
    """Serializer for Inventory"""
    total_quantity = serializers.ReadOnlyField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'available_quantity', 'reserved_quantity', 'damaged_quantity',
            'warehouse_location', 'procurement_sla', 'last_updated', 'total_quantity'
        ]


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listings"""
    
    class Meta:
        model = Listing
        fields = [
            'id', 'listing_id', 'marketplace', 'listing_status', 'fulfillment_type',
            'shipping_charges', 'is_cod_available', 'created_at', 'updated_at'
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Products"""
    inventory = InventorySerializer(read_only=True)
    listings = ListingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'sku', 'fsn', 'product_name', 'description', 'brand', 'category',
            'subcategory', 'mrp', 'hsn_code', 'tax_percentage', 'is_active',
            'created_at', 'updated_at', 'inventory', 'listings'
        ]
