from django.contrib import admin
from .models import Order, OrderItem, OrderCancellation


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'order_date', 'status', 'customer_name', 'total_amount', 'payment_method']
    list_filter = ['status', 'payment_method', 'order_date']
    search_fields = ['order_id', 'customer_name', 'customer_email', 'customer_phone']
    date_hierarchy = 'order_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'sku', 'product_name', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order']
    search_fields = ['sku', 'product_name', 'order__order_id']


@admin.register(OrderCancellation)
class OrderCancellationAdmin(admin.ModelAdmin):
    list_display = ['cancellation_id', 'order', 'cancelled_by', 'cancellation_date', 'refund_amount']
    list_filter = ['cancelled_by', 'cancellation_date']
    search_fields = ['cancellation_id', 'order__order_id', 'reason']
    date_hierarchy = 'cancellation_date'
