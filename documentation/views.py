from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import APIChangelog, APIEndpointDoc, SetupGuide
import json


class DocumentationHomeView(TemplateView):
    """Home page for documentation"""
    template_name = 'documentation/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apps'] = [
            {
                'name': 'Orders',
                'slug': 'orders',
                'description': 'Manage orders, cancellations, and order items',
                'icon': '📦'
            },
            {
                'name': 'Inventory',
                'slug': 'inventory',
                'description': 'Manage products, inventory levels, and listings',
                'icon': '📊'
            },
            {
                'name': 'Pricing',
                'slug': 'pricing',
                'description': 'Manage prices, pricing rules, and special promotions',
                'icon': '💰'
            },
            {
                'name': 'Returns',
                'slug': 'returns',
                'description': 'Handle returns, replacements, and refunds',
                'icon': '↩️'
            },
            {
                'name': 'Shipments',
                'slug': 'shipments',
                'description': 'Manage shipments, tracking, and courier partners',
                'icon': '🚚'
            },
            {
                'name': 'Reports',
                'slug': 'reports',
                'description': 'Generate and download various reports',
                'icon': '📈'
            },
        ]
        context['latest_version'] = APIChangelog.objects.first()
        context['total_endpoints'] = APIEndpointDoc.objects.count()
        return context


class SetupGuideView(ListView):
    """Setup guide page"""
    model = SetupGuide
    template_name = 'documentation/setup_guide.html'
    context_object_name = 'steps'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['installation_steps'] = SetupGuide.objects.filter(category='installation')
        context['configuration_steps'] = SetupGuide.objects.filter(category='configuration')
        context['testing_steps'] = SetupGuide.objects.filter(category='testing')
        context['deployment_steps'] = SetupGuide.objects.filter(category='deployment')
        return context


class APIDocumentationView(TemplateView):
    """API documentation page"""
    template_name = 'documentation/api_docs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_name = kwargs.get('app_name', 'orders')
        
        # Get endpoints for the selected app
        rest_endpoints = APIEndpointDoc.objects.filter(
            app_name=app_name, 
            protocol='REST'
        )
        soap_endpoints = APIEndpointDoc.objects.filter(
            app_name=app_name,
            protocol='SOAP'
        )
        
        context['app_name'] = app_name
        context['rest_endpoints'] = rest_endpoints
        context['soap_endpoints'] = soap_endpoints
        
        # Load from api_documentation.py if no DB entries
        if not rest_endpoints and not soap_endpoints:
            context['use_fallback'] = True
            context['fallback_data'] = self.get_fallback_docs(app_name)
        
        return context
    
    def get_fallback_docs(self, app_name):
        """Load documentation from api_documentation.py"""
        try:
            from api_documentation import API_DOCUMENTATION
            return API_DOCUMENTATION.get(app_name, {})
        except:
            return {}


class ChangelogView(ListView):
    """Changelog page"""
    model = APIChangelog
    template_name = 'documentation/changelog.html'
    context_object_name = 'versions'
    paginate_by = 10


class QuickStartView(TemplateView):
    """Quick start guide"""
    template_name = 'documentation/quick_start.html'


class APIReferenceView(TemplateView):
    """Complete API reference"""
    template_name = 'documentation/api_reference.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Load API documentation
        try:
            from api_documentation import API_DOCUMENTATION
            context['api_docs'] = API_DOCUMENTATION
        except:
            context['api_docs'] = {}
        
        return context


class TroubleshootingView(TemplateView):
    """Troubleshooting guide"""
    template_name = 'documentation/troubleshooting.html'
