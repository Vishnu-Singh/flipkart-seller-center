from django.db import models


class APIChangelog(models.Model):
    """Model to track API changes and version history"""
    version = models.CharField(max_length=20, unique=True)
    release_date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    changes = models.JSONField(help_text="JSON field containing list of changes")
    is_major = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-release_date']
        
    def __str__(self):
        return f"Version {self.version} - {self.title}"


class APIEndpointDoc(models.Model):
    """Model to document API endpoints"""
    app_name = models.CharField(max_length=50)
    endpoint_path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    protocol = models.CharField(max_length=10, choices=[('REST', 'REST'), ('SOAP', 'SOAP')])
    title = models.CharField(max_length=255)
    description = models.TextField()
    parameters = models.JSONField(help_text="JSON field for parameters documentation")
    example_request = models.TextField(blank=True)
    example_response = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_deprecated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['app_name', 'endpoint_path']
        
    def __str__(self):
        return f"{self.method} {self.endpoint_path}"


class SetupGuide(models.Model):
    """Model for setup instructions"""
    step_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    code_example = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('installation', 'Installation'),
        ('configuration', 'Configuration'),
        ('deployment', 'Deployment'),
        ('testing', 'Testing'),
    ])
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order', 'step_number']
        
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"
