from django.contrib import admin
from .models import APIChangelog, APIEndpointDoc, SetupGuide


@admin.register(APIChangelog)
class APIChangelogAdmin(admin.ModelAdmin):
    list_display = ['version', 'title', 'release_date', 'is_major', 'created_at']
    list_filter = ['is_major', 'release_date']
    search_fields = ['version', 'title', 'description']
    date_hierarchy = 'release_date'
    readonly_fields = ['created_at']


@admin.register(APIEndpointDoc)
class APIEndpointDocAdmin(admin.ModelAdmin):
    list_display = ['endpoint_path', 'method', 'protocol', 'app_name', 'title', 'is_deprecated']
    list_filter = ['protocol', 'app_name', 'method', 'is_deprecated']
    search_fields = ['endpoint_path', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SetupGuide)
class SetupGuideAdmin(admin.ModelAdmin):
    list_display = ['step_number', 'title', 'category', 'order']
    list_filter = ['category']
    search_fields = ['title', 'description']
    ordering = ['category', 'order', 'step_number']
