from rest_framework import serializers
from .models import Shipment, ShipmentTracking, ShippingLabel, CourierPartner


class ShipmentTrackingSerializer(serializers.ModelSerializer):
    """Serializer for Shipment Tracking"""
    
    class Meta:
        model = ShipmentTracking
        fields = ['id', 'event_date', 'location', 'event_description', 'status_code', 'created_at']


class ShippingLabelSerializer(serializers.ModelSerializer):
    """Serializer for Shipping Labels"""
    
    class Meta:
        model = ShippingLabel
        fields = ['id', 'label_url', 'label_format', 'generated_date', 'barcode']


class ShipmentSerializer(serializers.ModelSerializer):
    """Serializer for Shipments"""
    tracking_events = ShipmentTrackingSerializer(many=True, read_only=True)
    shipping_label = ShippingLabelSerializer(read_only=True)
    
    class Meta:
        model = Shipment
        fields = [
            'shipment_id', 'order', 'tracking_number', 'courier_partner', 'shipment_date',
            'expected_delivery_date', 'actual_delivery_date', 'status', 'pickup_address',
            'delivery_address', 'weight', 'dimensions', 'shipping_charges',
            'created_at', 'updated_at', 'tracking_events', 'shipping_label'
        ]


class CourierPartnerSerializer(serializers.ModelSerializer):
    """Serializer for Courier Partners"""
    
    class Meta:
        model = CourierPartner
        fields = [
            'id', 'partner_name', 'partner_code', 'contact_number',
            'email', 'service_type', 'is_active', 'created_at'
        ]
