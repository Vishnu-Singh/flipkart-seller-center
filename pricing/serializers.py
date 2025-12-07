from rest_framework import serializers
from .models import PricingRule, Price, SpecialPrice


class PricingRuleSerializer(serializers.ModelSerializer):
    """Serializer for Pricing Rules"""
    
    class Meta:
        model = PricingRule
        fields = [
            'id', 'product', 'rule_name', 'rule_type', 'value', 'percentage',
            'start_date', 'end_date', 'is_active', 'created_at', 'updated_at'
        ]


class PriceSerializer(serializers.ModelSerializer):
    """Serializer for Prices"""
    profit_margin = serializers.ReadOnlyField()
    
    class Meta:
        model = Price
        fields = [
            'id', 'product', 'listing_price', 'selling_price', 'discount_percentage',
            'cost_price', 'commission_percentage', 'shipping_fee', 'last_updated', 'profit_margin'
        ]


class SpecialPriceSerializer(serializers.ModelSerializer):
    """Serializer for Special Prices"""
    
    class Meta:
        model = SpecialPrice
        fields = [
            'id', 'product', 'special_price', 'start_date', 'end_date',
            'promotion_name', 'is_active', 'created_at'
        ]
