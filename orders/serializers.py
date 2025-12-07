from rest_framework import serializers
from .models import Order, OrderItem, OrderCancellation


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for Order Items"""
    
    class Meta:
        model = OrderItem
        fields = ['id', 'sku', 'product_name', 'quantity', 'unit_price', 'total_price', 'hsn_code']


class OrderCancellationSerializer(serializers.ModelSerializer):
    """Serializer for Order Cancellations"""
    
    class Meta:
        model = OrderCancellation
        fields = ['id', 'cancellation_id', 'reason', 'cancelled_by', 'cancellation_date', 'refund_amount']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Orders"""
    items = OrderItemSerializer(many=True, read_only=True)
    cancellations = OrderCancellationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'order_id', 'order_date', 'status', 'customer_name', 'customer_email',
            'customer_phone', 'shipping_address', 'billing_address', 'total_amount',
            'payment_method', 'created_at', 'updated_at', 'items', 'cancellations'
        ]
