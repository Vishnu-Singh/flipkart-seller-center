from django.db import models


class Product(models.Model):
    """Model for Products in Inventory"""
    sku = models.CharField(max_length=100, unique=True, primary_key=True)
    fsn = models.CharField(max_length=100, unique=True)  # Flipkart Serial Number
    product_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    hsn_code = models.CharField(max_length=20)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['product_name']
        
    def __str__(self):
        return f"{self.product_name} ({self.sku})"


class Inventory(models.Model):
    """Model for Inventory Stock"""
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    available_quantity = models.IntegerField(default=0)
    reserved_quantity = models.IntegerField(default=0)
    damaged_quantity = models.IntegerField(default=0)
    warehouse_location = models.CharField(max_length=100, blank=True, null=True)
    procurement_sla = models.IntegerField(help_text="Procurement SLA in days")
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Inventories"
        
    def __str__(self):
        return f"Inventory for {self.product.sku}"
    
    @property
    def total_quantity(self):
        return self.available_quantity + self.reserved_quantity + self.damaged_quantity


class Listing(models.Model):
    """Model for Product Listings"""
    LISTING_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('DELISTED', 'Delisted'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='listings')
    listing_id = models.CharField(max_length=100, unique=True)
    marketplace = models.CharField(max_length=50, default='Flipkart')
    listing_status = models.CharField(max_length=20, choices=LISTING_STATUS_CHOICES, default='ACTIVE')
    fulfillment_type = models.CharField(max_length=50)  # FBF or Self-Ship
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_cod_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Listing {self.listing_id} for {self.product.sku}"
