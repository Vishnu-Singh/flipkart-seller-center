from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
from .models import Report, ScheduledReport
from django.utils import timezone
from datetime import date, timedelta


class ReportsService(ServiceBase):
    """SOAP Service for Reports API"""
    
    @rpc(Unicode, _returns=Unicode)
    def get_report(ctx, report_id):
        """Get report details by report ID"""
        try:
            report = Report.objects.get(report_id=report_id)
            return f"Report ID: {report.report_id}, Type: {report.report_type}, Status: {report.status}, Format: {report.report_format}"
        except Report.DoesNotExist:
            return f"Report {report_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def get_report_status(ctx, report_id):
        """Get report generation status"""
        try:
            report = Report.objects.get(report_id=report_id)
            return f"Report {report_id} status: {report.status}"
        except Report.DoesNotExist:
            return f"Report {report_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def download_report(ctx, report_id):
        """Get report download URL"""
        try:
            report = Report.objects.get(report_id=report_id)
            if report.status == 'COMPLETED' and report.file_url:
                return f"Download URL: {report.file_url}, Size: {report.file_size} bytes"
            else:
                return f"Report {report_id} is not ready for download. Status: {report.status}"
        except Report.DoesNotExist:
            return f"Report {report_id} not found"
    
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def generate_report(ctx, report_type, report_format, requested_by):
        """Generate a new report"""
        report_id = f"RPT-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            report = Report.objects.create(
                report_id=report_id,
                report_type=report_type,
                report_name=f"{report_type} Report",
                report_format=report_format,
                status='IN_PROGRESS',
                start_date=date.today() - timedelta(days=30),
                end_date=date.today(),
                requested_by=requested_by
            )
            return f"Report generation initiated. Report ID: {report_id}"
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    @rpc(_returns=Unicode)
    def list_scheduled_reports(ctx):
        """List all active scheduled reports"""
        schedules = ScheduledReport.objects.filter(is_active=True)
        result = []
        for schedule in schedules:
            result.append(f"{schedule.schedule_id}: {schedule.report_name} ({schedule.frequency})")
        return ", ".join(result) if result else "No active scheduled reports found"
    
    @rpc(Unicode, _returns=Unicode)
    def get_scheduled_report(ctx, schedule_id):
        """Get scheduled report details"""
        try:
            schedule = ScheduledReport.objects.get(schedule_id=schedule_id)
            return f"Schedule ID: {schedule.schedule_id}, Report: {schedule.report_name}, Frequency: {schedule.frequency}, Next Run: {schedule.next_run_date}"
        except ScheduledReport.DoesNotExist:
            return f"Scheduled report {schedule_id} not found"
    
    @rpc(Unicode, _returns=Unicode)
    def run_scheduled_report(ctx, schedule_id):
        """Run a scheduled report immediately"""
        try:
            schedule = ScheduledReport.objects.get(schedule_id=schedule_id)
            
            report_id = f"RPT-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            report = Report.objects.create(
                report_id=report_id,
                report_type=schedule.report_type,
                report_name=schedule.report_name,
                report_format=schedule.report_format,
                status='IN_PROGRESS',
                start_date=date.today() - timedelta(days=30),
                end_date=date.today(),
                requested_by='System'
            )
            
            schedule.last_run_date = timezone.now()
            schedule.save()
            
            return f"Scheduled report executed. Report ID: {report_id}"
        except ScheduledReport.DoesNotExist:
            return f"Scheduled report {schedule_id} not found"


# Create SOAP application
reports_soap_app = Application(
    [ReportsService],
    tns='flipkart.seller.reports',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

reports_soap_application = csrf_exempt(DjangoApplication(reports_soap_app))
