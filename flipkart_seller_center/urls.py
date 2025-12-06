"""
URL configuration for flipkart_seller_center project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    """Home page with API documentation"""
    return JsonResponse({
        'message': 'Flipkart Seller Center API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'orders': {
                'rest': '/orders/api/',
                'soap': '/orders/soap/',
            },
            'inventory': {
                'rest': '/inventory/api/',
                'soap': '/inventory/soap/',
            },
            'pricing': {
                'rest': '/pricing/api/',
                'soap': '/pricing/soap/',
            },
            'returns': {
                'rest': '/returns/api/',
                'soap': '/returns/soap/',
            },
            'shipments': {
                'rest': '/shipments/api/',
                'soap': '/shipments/soap/',
            },
            'reports': {
                'rest': '/reports/api/',
                'soap': '/reports/soap/',
            },
        },
        'documentation': {
            'rest': 'Visit /orders/api/, /inventory/api/, etc. for browsable REST API',
            'soap': 'SOAP WSDL available at /orders/soap/?wsdl, /inventory/soap/?wsdl, etc.'
        }
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # Orders API (REST and SOAP)
    path('orders/', include('orders.urls')),
    
    # Inventory API (REST and SOAP)
    path('inventory/', include('inventory.urls')),
    
    # Pricing API (REST and SOAP)
    path('pricing/', include('pricing.urls')),
    
    # Returns API (REST and SOAP)
    path('returns/', include('returns.urls')),
    
    # Shipments API (REST and SOAP)
    path('shipments/', include('shipments.urls')),
    
    # Reports API (REST and SOAP)
    path('reports/', include('reports.urls')),
]
