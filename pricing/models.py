from django.db import models
from inventory.models import Product


class PricingRule(models.Model):
    """Model for Pricing Rules"""
    RULE_TYPE_CHOICES = [
        ('DISCOUNT', 'Discount'),
        ('MARKUP', 'Markup'),
        ('FIXED', 'Fixed Price'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pricing_rules')
    rule_name = models.CharField(max_length=255)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.rule_name} for {self.product.sku}"


class Price(models.Model):
    """Model for Product Pricing"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='price')
    listing_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Pricing for {self.product.sku}"
    
    @property
    def profit_margin(self):
        """Calculate profit margin"""
        profit = self.selling_price - self.cost_price - (self.selling_price * self.commission_percentage / 100) - self.shipping_fee
        return profit


class SpecialPrice(models.Model):
    """Model for Special Pricing/Promotions"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='special_prices')
    special_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    promotion_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
        
    def __str__(self):
        return f"{self.promotion_name} for {self.product.sku}"
