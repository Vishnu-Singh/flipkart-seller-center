from spyne import Application, rpc, ServiceBase, Unicode, Decimal
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from .models import Price, PricingRule, SpecialPrice
from inventory.models import Product


class PricingService(ServiceBase):
    """SOAP Service for Pricing API"""
    
    @rpc(Unicode, _returns=Unicode)
    def get_price(ctx, sku):
        """Get price details for a product"""
        try:
            product = Product.objects.get(sku=sku)
            price = product.price
            return f"SKU: {sku}, Listing Price: {price.listing_price}, Selling Price: {price.selling_price}, Discount: {price.discount_percentage}%"
        except Product.DoesNotExist:
            return f"Product {sku} not found"
        except Price.DoesNotExist:
            return f"Price not found for product {sku}"
    
    @rpc(Unicode, Decimal, _returns=Unicode)
    def update_selling_price(ctx, sku, new_price):
        """Update selling price for a product"""
        try:
            product = Product.objects.get(sku=sku)
            price = product.price
            price.selling_price = new_price
            
            # Recalculate discount percentage
            if price.listing_price > 0:
                price.discount_percentage = ((price.listing_price - new_price) / price.listing_price) * 100
            
            price.save()
            return f"Selling price updated for {sku}. New price: {new_price}, Discount: {price.discount_percentage}%"
        except Product.DoesNotExist:
            return f"Product {sku} not found"
        except Price.DoesNotExist:
            return f"Price not found for product {sku}"
    
    @rpc(Unicode, _returns=Unicode)
    def get_profit_margin(ctx, sku):
        """Calculate profit margin for a product"""
        try:
            product = Product.objects.get(sku=sku)
            price = product.price
            margin = price.profit_margin
            return f"SKU: {sku}, Profit Margin: {margin}"
        except Product.DoesNotExist:
            return f"Product {sku} not found"
        except Price.DoesNotExist:
            return f"Price not found for product {sku}"
    
    @rpc(Unicode, _returns=Unicode)
    def list_special_prices(ctx, sku):
        """List all special prices for a product"""
        try:
            product = Product.objects.get(sku=sku)
            special_prices = product.special_prices.filter(is_active=True)
            
            if special_prices.exists():
                result = []
                for sp in special_prices:
                    result.append(f"{sp.promotion_name}: {sp.special_price}")
                return ", ".join(result)
            else:
                return f"No active special prices for {sku}"
        except Product.DoesNotExist:
            return f"Product {sku} not found"


# Create SOAP application
pricing_soap_app = Application(
    [PricingService],
    tns='flipkart.seller.pricing',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

pricing_soap_application = DjangoApplication(pricing_soap_app)
