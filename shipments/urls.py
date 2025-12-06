from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShipmentViewSet, ShipmentTrackingViewSet,
    ShippingLabelViewSet, CourierPartnerViewSet
)
from .soap_views import shipments_soap_application

# REST API Router
router = DefaultRouter()
router.register(r'shipments', ShipmentViewSet, basename='shipment')
router.register(r'shipment-tracking', ShipmentTrackingViewSet, basename='shipmenttracking')
router.register(r'shipping-labels', ShippingLabelViewSet, basename='shippinglabel')
router.register(r'courier-partners', CourierPartnerViewSet, basename='courierpartner')

urlpatterns = [
    # REST API endpoints
    path('api/', include(router.urls)),
    
    # SOAP API endpoint
    path('soap/', shipments_soap_application),
]
