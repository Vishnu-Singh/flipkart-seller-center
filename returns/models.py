from django.db import models
from orders.models import Order, OrderItem


class Return(models.Model):
    """Model for Returns"""
    RETURN_STATUS_CHOICES = [
        ('INITIATED', 'Initiated'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PICKED_UP', 'Picked Up'),
        ('IN_TRANSIT', 'In Transit'),
        ('RECEIVED', 'Received'),
        ('REFUNDED', 'Refunded'),
        ('COMPLETED', 'Completed'),
    ]
    
    RETURN_REASON_CHOICES = [
        ('DEFECTIVE', 'Defective Product'),
        ('WRONG_ITEM', 'Wrong Item Delivered'),
        ('NOT_AS_DESCRIBED', 'Not as Described'),
        ('SIZE_ISSUE', 'Size/Fit Issue'),
        ('QUALITY_ISSUE', 'Quality Issue'),
        ('DAMAGED', 'Damaged'),
        ('OTHER', 'Other'),
    ]
    
    return_id = models.CharField(max_length=100, unique=True, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='returns')
    return_date = models.DateTimeField(auto_now_add=True)
    return_reason = models.CharField(max_length=50, choices=RETURN_REASON_CHOICES)
    return_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default='INITIATED')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-return_date']
        
    def __str__(self):
        return f"Return {self.return_id} for Order {self.order.order_id}"


class Replacement(models.Model):
    """Model for Replacements"""
    REPLACEMENT_STATUS_CHOICES = [
        ('INITIATED', 'Initiated'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISPATCHED', 'Dispatched'),
        ('DELIVERED', 'Delivered'),
        ('COMPLETED', 'Completed'),
    ]
    
    replacement_id = models.CharField(max_length=100, unique=True, primary_key=True)
    return_request = models.OneToOneField(Return, on_delete=models.CASCADE, related_name='replacement')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='replacements')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='replacements')
    replacement_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REPLACEMENT_STATUS_CHOICES, default='INITIATED')
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-replacement_date']
        
    def __str__(self):
        return f"Replacement {self.replacement_id} for Return {self.return_request.return_id}"


class RefundTransaction(models.Model):
    """Model for Refund Transactions"""
    REFUND_METHOD_CHOICES = [
        ('ORIGINAL_PAYMENT', 'Original Payment Method'),
        ('WALLET', 'Wallet'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    ]
    
    REFUND_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    transaction_id = models.CharField(max_length=100, unique=True, primary_key=True)
    return_request = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='refund_transactions')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_method = models.CharField(max_length=50, choices=REFUND_METHOD_CHOICES)
    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='PENDING')
    transaction_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-transaction_date']
        
    def __str__(self):
        return f"Refund {self.transaction_id} for Return {self.return_request.return_id}"
