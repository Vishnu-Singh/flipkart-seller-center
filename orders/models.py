from django.db import models


class Order(models.Model):
    """Model for Flipkart Orders"""
    STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('PACKED', 'Packed'),
        ('READY_TO_DISPATCH', 'Ready to Dispatch'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('RETURNED', 'Returned'),
    ]
    
    order_id = models.CharField(max_length=100, unique=True, primary_key=True)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.TextField()
    billing_address = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order_date']
        
    def __str__(self):
        return f"Order {self.order_id}"


class OrderItem(models.Model):
    """Model for Order Items"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    hsn_code = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        ordering = ['order', 'sku']
        
    def __str__(self):
        return f"{self.product_name} (x{self.quantity})"


class OrderCancellation(models.Model):
    """Model for Order Cancellations"""
    order = models.ForeignKey(Order, related_name='cancellations', on_delete=models.CASCADE)
    cancellation_id = models.CharField(max_length=100, unique=True)
    reason = models.TextField()
    cancelled_by = models.CharField(max_length=50)  # SELLER or CUSTOMER
    cancellation_date = models.DateTimeField(auto_now_add=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Cancellation {self.cancellation_id} for Order {self.order.order_id}"
