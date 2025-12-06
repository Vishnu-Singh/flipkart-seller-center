from django.db import models
from orders.models import Order


class Shipment(models.Model):
    """Model for Shipments"""
    SHIPMENT_STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PACKED', 'Packed'),
        ('READY_TO_SHIP', 'Ready to Ship'),
        ('SHIPPED', 'Shipped'),
        ('IN_TRANSIT', 'In Transit'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('RETURNED', 'Returned'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    shipment_id = models.CharField(max_length=100, unique=True, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipments')
    tracking_number = models.CharField(max_length=100, unique=True)
    courier_partner = models.CharField(max_length=100)
    shipment_date = models.DateTimeField()
    expected_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=SHIPMENT_STATUS_CHOICES, default='CREATED')
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in kg")
    dimensions = models.CharField(max_length=100, help_text="LxWxH in cm")
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-shipment_date']
        
    def __str__(self):
        return f"Shipment {self.shipment_id} for Order {self.order.order_id}"


class ShipmentTracking(models.Model):
    """Model for Shipment Tracking Events"""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='tracking_events')
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    event_description = models.TextField()
    status_code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-event_date']
        
    def __str__(self):
        return f"Tracking for {self.shipment.shipment_id} at {self.location}"


class ShippingLabel(models.Model):
    """Model for Shipping Labels"""
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE, related_name='shipping_label')
    label_url = models.URLField()
    label_format = models.CharField(max_length=20, default='PDF')
    generated_date = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Label for Shipment {self.shipment.shipment_id}"


class CourierPartner(models.Model):
    """Model for Courier Partners"""
    partner_name = models.CharField(max_length=100, unique=True)
    partner_code = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    service_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.partner_name
