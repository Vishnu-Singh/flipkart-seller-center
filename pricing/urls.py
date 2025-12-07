from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PricingRuleViewSet, PriceViewSet, SpecialPriceViewSet
from .soap_views import pricing_soap_application

# REST API Router
router = DefaultRouter()
router.register(r'pricing-rules', PricingRuleViewSet, basename='pricingrule')
router.register(r'prices', PriceViewSet, basename='price')
router.register(r'special-prices', SpecialPriceViewSet, basename='specialprice')

urlpatterns = [
    # REST API endpoints
    path('api/', include(router.urls)),
    
    # SOAP API endpoint
    path('soap/', pricing_soap_application),
]
