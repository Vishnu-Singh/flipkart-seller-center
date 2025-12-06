from django.db import models


class Report(models.Model):
    """Model for Reports"""
    REPORT_TYPE_CHOICES = [
        ('SALES', 'Sales Report'),
        ('ORDERS', 'Orders Report'),
        ('INVENTORY', 'Inventory Report'),
        ('RETURNS', 'Returns Report'),
        ('SHIPMENTS', 'Shipments Report'),
        ('FINANCIAL', 'Financial Report'),
        ('PERFORMANCE', 'Performance Report'),
    ]
    
    REPORT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    REPORT_FORMAT_CHOICES = [
        ('CSV', 'CSV'),
        ('XLSX', 'Excel'),
        ('PDF', 'PDF'),
        ('JSON', 'JSON'),
    ]
    
    report_id = models.CharField(max_length=100, unique=True, primary_key=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    report_name = models.CharField(max_length=255)
    report_format = models.CharField(max_length=10, choices=REPORT_FORMAT_CHOICES)
    status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='PENDING')
    start_date = models.DateField()
    end_date = models.DateField()
    file_url = models.URLField(blank=True, null=True)
    file_size = models.BigIntegerField(null=True, blank=True, help_text="File size in bytes")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    requested_by = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.report_name} ({self.report_id})"


class ScheduledReport(models.Model):
    """Model for Scheduled Reports"""
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
    ]
    
    schedule_id = models.CharField(max_length=100, unique=True, primary_key=True)
    report_type = models.CharField(max_length=20, choices=Report.REPORT_TYPE_CHOICES)
    report_name = models.CharField(max_length=255)
    report_format = models.CharField(max_length=10, choices=Report.REPORT_FORMAT_CHOICES)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    next_run_date = models.DateTimeField()
    last_run_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    email_recipients = models.TextField(help_text="Comma-separated email addresses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['next_run_date']
        
    def __str__(self):
        return f"{self.report_name} - {self.frequency}"


class ReportMetrics(models.Model):
    """Model for Report Metrics"""
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='metrics')
    total_records = models.IntegerField(default=0)
    processing_time = models.DecimalField(max_digits=10, decimal_places=2, help_text="Processing time in seconds")
    data_range_start = models.DateTimeField()
    data_range_end = models.DateTimeField()
    filters_applied = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Metrics for {self.report.report_id}"
