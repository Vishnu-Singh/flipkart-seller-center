from django.contrib import admin
from .models import Shipment, ShipmentTracking, ShippingLabel, CourierPartner


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['shipment_id', 'order', 'tracking_number', 'courier_partner', 'status', 'shipment_date', 'expected_delivery_date']
    list_filter = ['status', 'courier_partner']
    search_fields = ['shipment_id', 'tracking_number', 'order__order_id']
    date_hierarchy = 'shipment_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ShipmentTracking)
class ShipmentTrackingAdmin(admin.ModelAdmin):
    list_display = ['shipment', 'event_date', 'location', 'status_code', 'event_description']
    list_filter = ['status_code', 'event_date']
    search_fields = ['shipment__shipment_id', 'shipment__tracking_number', 'location']
    date_hierarchy = 'event_date'
    readonly_fields = ['created_at']


@admin.register(ShippingLabel)
class ShippingLabelAdmin(admin.ModelAdmin):
    list_display = ['shipment', 'label_format', 'barcode', 'generated_date']
    search_fields = ['shipment__shipment_id', 'barcode']
    readonly_fields = ['generated_date']


@admin.register(CourierPartner)
class CourierPartnerAdmin(admin.ModelAdmin):
    list_display = ['partner_name', 'partner_code', 'service_type', 'contact_number', 'is_active']
    list_filter = ['is_active', 'service_type']
    search_fields = ['partner_name', 'partner_code', 'contact_number']
    readonly_fields = ['created_at']
