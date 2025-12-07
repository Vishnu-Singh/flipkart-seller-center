from rest_framework import serializers
from .models import Return, Replacement, RefundTransaction


class ReturnSerializer(serializers.ModelSerializer):
    """Serializer for Returns"""
    
    class Meta:
        model = Return
        fields = [
            'return_id', 'order', 'order_item', 'return_date', 'return_reason',
            'return_description', 'status', 'refund_amount', 'pickup_address',
            'created_at', 'updated_at'
        ]


class ReplacementSerializer(serializers.ModelSerializer):
    """Serializer for Replacements"""
    
    class Meta:
        model = Replacement
        fields = [
            'replacement_id', 'return_request', 'order', 'order_item',
            'replacement_date', 'status', 'tracking_id', 'delivery_address',
            'created_at', 'updated_at'
        ]


class RefundTransactionSerializer(serializers.ModelSerializer):
    """Serializer for Refund Transactions"""
    
    class Meta:
        model = RefundTransaction
        fields = [
            'transaction_id', 'return_request', 'refund_amount', 'refund_method',
            'refund_status', 'transaction_date', 'completed_date'
        ]
