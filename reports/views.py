from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Report, ScheduledReport, ReportMetrics
from .serializers import ReportSerializer, ScheduledReportSerializer, ReportMetricsSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Reports API
    
    Endpoints:
    - GET /api/reports/ - List all reports
    - POST /api/reports/ - Create/generate a report
    - GET /api/reports/{report_id}/ - Get report details
    - PUT /api/reports/{report_id}/ - Update report
    - DELETE /api/reports/{report_id}/ - Delete report
    - GET /api/reports/{report_id}/download/ - Download report
    - POST /api/reports/{report_id}/regenerate/ - Regenerate report
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download a report"""
        report = self.get_object()
        
        if report.status != 'COMPLETED':
            return Response(
                {'error': 'Report is not ready for download'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not report.file_url:
            return Response(
                {'error': 'Report file not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'report_id': report.report_id,
            'file_url': report.file_url,
            'file_size': report.file_size,
            'format': report.report_format
        })
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """Regenerate a report"""
        report = self.get_object()
        report.status = 'IN_PROGRESS'
        report.file_url = None
        report.save()
        
        # In a real implementation, this would trigger an async task
        # For now, we'll just simulate the process
        
        return Response({
            'message': f'Report {report.report_id} regeneration initiated',
            'status': report.status
        })


class ScheduledReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Scheduled Reports API
    
    Endpoints:
    - GET /api/scheduled-reports/ - List all scheduled reports
    - POST /api/scheduled-reports/ - Create a scheduled report
    - GET /api/scheduled-reports/{schedule_id}/ - Get scheduled report details
    - PUT /api/scheduled-reports/{schedule_id}/ - Update scheduled report
    - DELETE /api/scheduled-reports/{schedule_id}/ - Delete scheduled report
    - POST /api/scheduled-reports/{schedule_id}/activate/ - Activate schedule
    - POST /api/scheduled-reports/{schedule_id}/deactivate/ - Deactivate schedule
    - POST /api/scheduled-reports/{schedule_id}/run-now/ - Run report immediately
    """
    queryset = ScheduledReport.objects.all()
    serializer_class = ScheduledReportSerializer
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a scheduled report"""
        scheduled_report = self.get_object()
        scheduled_report.is_active = True
        scheduled_report.save()
        return Response({
            'message': f'Scheduled report {scheduled_report.schedule_id} activated'
        })
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a scheduled report"""
        scheduled_report = self.get_object()
        scheduled_report.is_active = False
        scheduled_report.save()
        return Response({
            'message': f'Scheduled report {scheduled_report.schedule_id} deactivated'
        })
    
    @action(detail=True, methods=['post'])
    def run_now(self, request, pk=None):
        """Run scheduled report immediately"""
        scheduled_report = self.get_object()
        
        # Create a new report instance
        from datetime import date, timedelta
        
        report = Report.objects.create(
            report_id=f"RPT-{timezone.now().strftime('%Y%m%d%H%M%S')}",
            report_type=scheduled_report.report_type,
            report_name=scheduled_report.report_name,
            report_format=scheduled_report.report_format,
            status='IN_PROGRESS',
            start_date=date.today() - timedelta(days=30),
            end_date=date.today(),
            requested_by='System'
        )
        
        scheduled_report.last_run_date = timezone.now()
        scheduled_report.save()
        
        return Response({
            'message': f'Report generation initiated',
            'report_id': report.report_id
        })


class ReportMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Report Metrics (Read-only)"""
    queryset = ReportMetrics.objects.all()
    serializer_class = ReportMetricsSerializer
