from django.contrib import admin
from .models import Return, Replacement, RefundTransaction


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ['return_id', 'order', 'return_reason', 'status', 'refund_amount', 'return_date']
    list_filter = ['status', 'return_reason']
    search_fields = ['return_id', 'order__order_id']
    date_hierarchy = 'return_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ['replacement_id', 'return_request', 'order', 'status', 'tracking_id', 'replacement_date']
    list_filter = ['status']
    search_fields = ['replacement_id', 'tracking_id', 'order__order_id']
    date_hierarchy = 'replacement_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RefundTransaction)
class RefundTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'return_request', 'refund_amount', 'refund_method', 'refund_status', 'transaction_date']
    list_filter = ['refund_method', 'refund_status']
    search_fields = ['transaction_id', 'return_request__return_id']
    date_hierarchy = 'transaction_date'
    readonly_fields = ['transaction_date', 'completed_date']
