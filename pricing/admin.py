from django.contrib import admin
from .models import PricingRule, Price, SpecialPrice


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ['rule_name', 'product', 'rule_type', 'value', 'percentage', 'is_active', 'start_date', 'end_date']
    list_filter = ['rule_type', 'is_active']
    search_fields = ['rule_name', 'product__sku', 'product__product_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'listing_price', 'selling_price', 'discount_percentage', 'profit_margin', 'last_updated']
    search_fields = ['product__sku', 'product__product_name']
    readonly_fields = ['last_updated', 'profit_margin']


@admin.register(SpecialPrice)
class SpecialPriceAdmin(admin.ModelAdmin):
    list_display = ['promotion_name', 'product', 'special_price', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['promotion_name', 'product__sku', 'product__product_name']
    readonly_fields = ['created_at']
