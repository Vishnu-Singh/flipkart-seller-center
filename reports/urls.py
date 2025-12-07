from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, ScheduledReportViewSet, ReportMetricsViewSet
from .soap_views import reports_soap_application

# REST API Router
router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')
router.register(r'scheduled-reports', ScheduledReportViewSet, basename='scheduledreport')
router.register(r'report-metrics', ReportMetricsViewSet, basename='reportmetrics')

urlpatterns = [
    # REST API endpoints
    path('api/', include(router.urls)),
    
    # SOAP API endpoint
    path('soap/', reports_soap_application),
]
