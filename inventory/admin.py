from django.contrib import admin
from .models import Product, Inventory, Listing


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['sku', 'fsn', 'product_name', 'brand', 'category', 'mrp', 'is_active']
    list_filter = ['is_active', 'brand', 'category']
    search_fields = ['sku', 'fsn', 'product_name', 'brand']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'available_quantity', 'reserved_quantity', 'damaged_quantity', 'total_quantity', 'last_updated']
    list_filter = ['warehouse_location']
    search_fields = ['product__sku', 'product__product_name']
    readonly_fields = ['last_updated', 'total_quantity']


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['listing_id', 'product', 'marketplace', 'listing_status', 'fulfillment_type', 'is_cod_available']
    list_filter = ['listing_status', 'marketplace', 'fulfillment_type', 'is_cod_available']
    search_fields = ['listing_id', 'product__sku', 'product__product_name']
    readonly_fields = ['created_at', 'updated_at']
