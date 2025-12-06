from rest_framework import serializers
from .models import Report, ScheduledReport, ReportMetrics


class ReportMetricsSerializer(serializers.ModelSerializer):
    """Serializer for Report Metrics"""
    
    class Meta:
        model = ReportMetrics
        fields = [
            'id', 'total_records', 'processing_time', 'data_range_start',
            'data_range_end', 'filters_applied', 'created_at'
        ]


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for Reports"""
    metrics = ReportMetricsSerializer(read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'report_id', 'report_type', 'report_name', 'report_format', 'status',
            'start_date', 'end_date', 'file_url', 'file_size', 'created_at',
            'completed_at', 'requested_by', 'metrics'
        ]


class ScheduledReportSerializer(serializers.ModelSerializer):
    """Serializer for Scheduled Reports"""
    
    class Meta:
        model = ScheduledReport
        fields = [
            'schedule_id', 'report_type', 'report_name', 'report_format', 'frequency',
            'next_run_date', 'last_run_date', 'is_active', 'email_recipients',
            'created_at', 'updated_at'
        ]
