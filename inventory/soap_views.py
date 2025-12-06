from spyne import Application, rpc, ServiceBase, Unicode, Integer, Decimal, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from .models import Product, Inventory, Listing


class InventoryService(ServiceBase):
    """SOAP Service for Inventory API"""
    
    @rpc(Unicode, _returns=Unicode)
    def get_product(ctx, sku):
        """Get product details by SKU"""
        try:
            product = Product.objects.get(sku=sku)
            return f"SKU: {product.sku}, Name: {product.product_name}, MRP: {product.mrp}, Active: {product.is_active}"
        except Product.DoesNotExist:
            return f"Product {sku} not found"
    
    @rpc(_returns=Unicode)
    def list_products(ctx):
        """List all products"""
        products = Product.objects.filter(is_active=True)[:10]
        result = []
        for product in products:
            result.append(f"{product.sku}: {product.product_name}")
        return ", ".join(result) if result else "No products found"
    
    @rpc(Unicode, _returns=Unicode)
    def get_inventory(ctx, sku):
        """Get inventory details by product SKU"""
        try:
            product = Product.objects.get(sku=sku)
            inventory = product.inventory
            return f"SKU: {sku}, Available: {inventory.available_quantity}, Reserved: {inventory.reserved_quantity}, Total: {inventory.total_quantity}"
        except Product.DoesNotExist:
            return f"Product {sku} not found"
        except Inventory.DoesNotExist:
            return f"Inventory not found for product {sku}"
    
    @rpc(Unicode, Integer, _returns=Unicode)
    def update_stock(ctx, sku, available_quantity):
        """Update stock levels for a product"""
        try:
            product = Product.objects.get(sku=sku)
            inventory = product.inventory
            inventory.available_quantity = available_quantity
            inventory.save()
            return f"Stock updated for {sku}. New available quantity: {available_quantity}"
        except Product.DoesNotExist:
            return f"Product {sku} not found"
        except Inventory.DoesNotExist:
            return f"Inventory not found for product {sku}"
    
    @rpc(Unicode, _returns=Unicode)
    def activate_product(ctx, sku):
        """Activate a product"""
        try:
            product = Product.objects.get(sku=sku)
            product.is_active = True
            product.save()
            return f"Product {sku} activated successfully"
        except Product.DoesNotExist:
            return f"Product {sku} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def deactivate_product(ctx, sku):
        """Deactivate a product"""
        try:
            product = Product.objects.get(sku=sku)
            product.is_active = False
            product.save()
            return f"Product {sku} deactivated successfully"
        except Product.DoesNotExist:
            return f"Product {sku} not found"


# Create SOAP application
inventory_soap_app = Application(
    [InventoryService],
    tns='flipkart.seller.inventory',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

inventory_soap_application = DjangoApplication(inventory_soap_app)
