from django.contrib import admin
from .models import Report, ScheduledReport, ReportMetrics


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_id', 'report_name', 'report_type', 'report_format', 'status', 'created_at', 'completed_at']
    list_filter = ['report_type', 'report_format', 'status']
    search_fields = ['report_id', 'report_name', 'requested_by']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'completed_at']


@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = ['schedule_id', 'report_name', 'report_type', 'frequency', 'next_run_date', 'is_active']
    list_filter = ['report_type', 'frequency', 'is_active']
    search_fields = ['schedule_id', 'report_name']
    readonly_fields = ['created_at', 'updated_at', 'last_run_date']


@admin.register(ReportMetrics)
class ReportMetricsAdmin(admin.ModelAdmin):
    list_display = ['report', 'total_records', 'processing_time', 'data_range_start', 'data_range_end']
    search_fields = ['report__report_id', 'report__report_name']
    readonly_fields = ['created_at']
